# coding: utf-8


# from vo.response.base_response import BaseResponse,PositionEntity,WordEntity,ProbEntity
from app.main.app.vo.response.base_response import BaseResponse


class IdcardResponse(BaseResponse):
    """
     结果返回报文
    """
    # 当前请求id
    sid = ''
