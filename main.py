from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register(
    name="pjskbl",
    author="Your Name",
    description="倍率计算插件，用于计算模拟卡组的倍率和技能实际值",
    version="1.0.0",
    repository="https://github.com/banana417/pjskbl"
)
class RateCalculatorPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        logger.info("倍率计算插件已加载")

    @filter.command("倍率")
    async def calculate_rate(self, event: AstrMessageEvent):
        '''处理倍率计算指令，格式: 倍率 数字1 数字2 数字3 数字4 数字5'''
        try:
            # 获取消息内容并分割参数
            message = event.message_str.strip()
            params = message.split()[1:6]  # 获取指令后的5个参数

            if len(params) != 5:
                yield event.plain_result("参数格式错误！请使用: 倍率 数字1 数字2 数字3 数字4 数字5")
                return

            # 转换为数字
            nums = list(map(float, params))
            num1, num2, num3, num4, num5 = nums

            # 执行计算
            result1 = num1 + (num2 + num3 + num4 + num5) * 0.2
            result2 = result1 * 0.01 + 1

            # 格式化输出结果
            response = f"您的模拟卡组：倍率为{result2:.2f}:技能实际值为{result1:.2f}"
            yield event.plain_result(response)

        except ValueError:
            yield event.plain_result("参数错误！请确保所有参数都是数字")
        except Exception as e:
            logger.error(f"计算出错: {str(e)}")
            yield event.plain_result("计算过程中发生错误，请稍后再试")

    async def terminate(self):
        logger.info("倍率计算插件已卸载")