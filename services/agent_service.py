from sqlalchemy.orm import Session
import models
from langchain_openai import ChatOpenAI
from langchain_classic.agents import AgentExecutor, create_tool_calling_agent
from langchain_core.prompts import ChatPromptTemplate
from langchain.tools import tool

# 1. 纯 Python 业务函数（查库、建单）
def db_query_order(order_sn: str, db: Session):
    order = db.query(models.Order).filter(models.Order.order_sn == order_sn).first()
    if not order:
        return None
    return f"订单 {order_sn}：商品 {order.product_name}，金额 {order.amount} 元，当前状态【{order.status}】。"

def db_refund_order(order_sn: str, issue_desc: str, db: Session):
    order = db.query(models.Order).filter(models.Order.order_sn == order_sn).first()
    if not order:
        return "建单失败：订单不存在。"
    if order.status == "已退款":
        return "建单失败：该订单已退款，请勿重复操作！"
    
    order.status = "待审核"
    new_ticket = models.Ticket(order_id=order.id, issue_desc=issue_desc, status="待审核")
    db.add(new_ticket)
    db.commit()
    return f"退款申请已成功提交，工单号 TK-{new_ticket.id}，等待后台主管审核。"

# 2. 工具工厂（把数据库藏起来，把工具给 AI）
def get_tools(db: Session):
    @tool
    def query_order_tool(order_sn: str) -> str:
        """根据订单号查询订单状态。"""
        return db_query_order(order_sn, db)

    @tool
    def refund_order_tool(order_sn: str, issue_desc: str) -> str:
        """当确认订单存在且未退款时，帮用户申请退款建单。"""
        return db_refund_order(order_sn, issue_desc, db)

    return [query_order_tool, refund_order_tool]

# 3. 核心 Agent 调度
def run_agent(message: str, db: Session):
    tools = get_tools(db)
    llm = ChatOpenAI(model="deepseek-chat", temperature=0)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", "你是一个专业的企业售后客服 AI。1. 提取订单号。2. 先调用 query_order_tool 查询。3. 确认存在且未退款后，调用 refund_order_tool 建单。绝对不要凭空捏造！"),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ])
    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    
    response = agent_executor.invoke({"input": message})
    return response["output"]