from Valorant import *
with open('Valorant.val', 'r', encoding='utf-8') as f:
    测试脚本 =f.read()

编译结果 = 战术编译器.编译(测试脚本)

print('运行时间0.000000000000000000000000114514ms!s')

#print("✅ 编译成功:\n" + 编译结果)

        # 执行阶段

战场状态 = 战术执行器.安全执行(编译结果)