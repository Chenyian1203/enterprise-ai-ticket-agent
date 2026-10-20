from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
import models, schemas, auth
from database import get_db

# =====================================================================
# 【企业重点 1：创建路由器】
# 这里必须定义一个名叫 router 的变量，main.py 才能找到它并挂载。
# prefix 表示这个文件里的接口，都会自带 /api/orders 前缀。
# =====================================================================
router = APIRouter(prefix="/api/orders", tags=["订单业务"])

# =====================================================================
# 【企业重点 2：带安全认证的查单接口】
# Depends(auth.get_current_user) 是门票，没带 Token 的黑客进不来。
# =====================================================================
@router.get("/query/{order_sn}")
def query_order(
    order_sn: str, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(auth.get_current_user)
):
    # 去数据库里找这个订单号
    order = db.query(models.Order).filter(models.Order.order_sn == order_sn).first()
    
    if not order:
        # 【企业重点：防 AI 幻觉】找不到就直接报 404，绝对不让大模型瞎编
        raise HTTPException(status_code=404, detail=f"未找到订单号为 {order_sn} 的记录，请核对。")
    
    return {
        "code": 200,
        "message": "查询成功",
        "data": {
            "order_sn": order.order_sn,
            "product_name": order.product_name,
            "amount": order.amount,
            "status": order.status
        }
    }

# =====================================================================
# 【企业重点 3：带风控的退款建单接口】
# =====================================================================
@router.post("/refund")
def apply_refund(
    data: schemas.RefundApply, 
    db: Session = Depends(get_db), 
    current_user: str = Depends(auth.get_current_user)
):
    # 1. 先查订单在不在
    order = db.query(models.Order).filter(models.Order.order_sn == data.order_sn).first()
    if not order:
        raise HTTPException(status_code=404, detail="订单不存在")
    
    # 2. 核心风控：如果订单已经是“已退款”状态，坚决不给建单
    if order.status == "已退款":
        return {"code": 400, "message": "该订单已处于退款完成状态，无法重复退款！"}

    # 3. 更新订单状态为“待审核”
    order.status = "待审核"
    
    # 4. 真正的业务逻辑：生成一条工单记录存入数据库
    new_ticket = models.Ticket(
        order_id=order.id,
        issue_desc=data.issue_desc,
        status="待审核"
    )
    db.add(new_ticket)
    db.commit()
    db.refresh(new_ticket)
    
    return {
        "code": 200, 
        "message": "退款工单创建成功，等待后台主管审核",
        "ticket_id": new_ticket.id,
        "order_sn": order.order_sn
    }