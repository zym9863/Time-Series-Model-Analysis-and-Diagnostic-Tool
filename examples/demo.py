#!/usr/bin/env python3
"""
时间序列模型分析与诊断工具 - 完整功能演示

本演示脚本展示了tsdiag工具的所有主要功能。
"""

import tsdiag
import numpy as np


def demo_header(title):
    """打印演示标题"""
    print("\n" + "=" * 60)
    print(f" {title}")
    print("=" * 60)


def demo_section(title):
    """打印演示小节标题"""
    print(f"\n{title}")
    print("-" * len(title))


def main():
    print("🚀 时间序列模型分析与诊断工具 - 完整功能演示")
    
    # 1. 基本功能演示
    demo_header("1. 基本功能演示")
    
    demo_section("AR模型平稳性检验")
    
    # 测试不同的AR模型
    ar_examples = [
        ([0.5], "平稳的AR(1)"),
        ([1.1], "非平稳的AR(1)"),
        ([1.0], "单位根AR(1)"),
        ([0.5, -0.3], "平稳的AR(2)"),
        ([1.2, -0.1], "非平稳的AR(2)")
    ]
    
    for coeffs, description in ar_examples:
        result = tsdiag.stationarity_check(coeffs)
        status = "✅ 平稳" if result.is_stationary else "❌ 非平稳"
        print(f"{description:15} {coeffs}: {status}")
    
    demo_section("MA模型可逆性检验")
    
    # 测试不同的MA模型
    ma_examples = [
        ([0.5], "可逆的MA(1)"),
        ([1.1], "不可逆的MA(1)"),
        ([1.0], "单位根MA(1)"),
        ([0.5, 0.3], "可逆的MA(2)"),
        ([1.2, 0.1], "不可逆的MA(2)")
    ]
    
    for coeffs, description in ma_examples:
        result = tsdiag.invertibility_check(coeffs)
        status = "✅ 可逆" if result.is_invertible else "❌ 不可逆"
        print(f"{description:15} {coeffs}: {status}")
    
    # 2. 高级API演示
    demo_header("2. 高级API演示")
    
    demo_section("TSModelDiagnostic类使用")
    
    diagnostic = tsdiag.TSModelDiagnostic()
    
    # 检验ARMA模型
    ar_result, ma_result = diagnostic.check_arma_model(
        ar_coefficients=[0.5, -0.3],
        ma_coefficients=[0.4, 0.2],
        verbose=False
    )
    
    summary = diagnostic.get_summary()
    print("ARMA(2,2)模型检验结果:")
    print(f"  AR部分平稳: {'是' if summary['ar_stationary'] else '否'}")
    print(f"  MA部分可逆: {'是' if summary['ma_invertible'] else '否'}")
    print(f"  整体有效: {'是' if summary['arma_valid'] else '否'}")
    
    demo_section("快速检验功能")
    
    quick_tests = [
        ([0.5], "AR(1)"),
        ([0.8, 0.15], "AR(2)"),
        ([1.1], "AR(1)不稳定")
    ]
    
    for coeffs, desc in quick_tests:
        is_stationary = tsdiag.quick_ar_check(coeffs)
        is_invertible = tsdiag.quick_ma_check(coeffs)
        print(f"{desc:15}: AR平稳={is_stationary}, MA可逆={is_invertible}")
    
    # 3. 稳定性分析演示
    demo_header("3. 稳定性分析演示")
    
    demo_section("稳定性边际分析")
    
    stability_tests = [
        [0.3],    # 低风险
        [0.95],   # 中等风险
        [1.05],   # 高风险
    ]
    
    for coeffs in stability_tests:
        analysis = tsdiag.analyze_model_stability(ar_coefficients=coeffs)
        ar_info = analysis['ar']
        
        print(f"AR模型 {coeffs}:")
        print(f"  稳定性边际: {ar_info['stability_margin']:.3f}")
        print(f"  风险等级: {ar_info['risk_level']}")
        print(f"  平稳性: {'是' if ar_info['is_stationary'] else '否'}")
    
    # 4. 批量分析演示
    demo_header("4. 批量分析演示")
    
    demo_section("批量AR模型分析")
    
    ar_models = [
        [0.5],
        [1.1], 
        [0.5, -0.3],
        [1.2, -0.1]
    ]
    
    ar_names = ["稳定AR(1)", "不稳定AR(1)", "稳定AR(2)", "不稳定AR(2)"]
    
    batch_results = tsdiag.batch_stationarity_check(ar_models, ar_names)
    
    print(f"{'模型':<12} {'平稳性':<8} {'边际':<8} {'风险':<8}")
    print("-" * 40)
    
    for result in batch_results:
        if 'error' not in result:
            name = result['model_name']
            stationary = "是" if result['is_stationary'] else "否"
            margin = f"{result['stability_margin']:.3f}"
            risk = result['risk_level']
            print(f"{name:<12} {stationary:<8} {margin:<8} {risk:<8}")
    
    demo_section("MA模型比较")
    
    ma_models = [[0.5], [1.1], [0.3], [1.5]]
    ma_names = ["可逆1", "不可逆1", "可逆2", "不可逆2"]
    
    comparison = tsdiag.compare_ma_models(ma_models, ma_names)
    
    print(f"总模型数: {comparison['total_models']}")
    print(f"可逆模型数: {comparison['invertible_models']}")
    print(f"可逆性比率: {comparison['invertibility_rate']:.1%}")
    
    if comparison['best_model']:
        print(f"最佳模型: {comparison['best_model']['model_name']}")
    
    # 5. 修改建议演示
    demo_header("5. 修改建议演示")
    
    demo_section("AR模型修改建议")
    
    problematic_ar = [1.1]
    suggestions = tsdiag.suggest_ar_modifications(problematic_ar)
    
    print(f"原始模型: {problematic_ar}")
    print("修改建议:")
    for suggestion in suggestions['suggestions']:
        print(f"  • {suggestion}")
    
    if 'suggested_coefficients' in suggestions:
        new_coeffs = suggestions['suggested_coefficients']
        print(f"建议系数: {new_coeffs}")
        
        # 验证修改后的模型
        new_result = tsdiag.stationarity_check(new_coeffs)
        print(f"修改后平稳性: {'是' if new_result.is_stationary else '否'}")
    
    demo_section("MA模型修改建议")
    
    problematic_ma = [1.2]
    ma_suggestions = tsdiag.suggest_ma_modifications(problematic_ma)
    
    print(f"原始模型: {problematic_ma}")
    print("修改建议:")
    for suggestion in ma_suggestions['suggestions']:
        print(f"  • {suggestion}")
    
    if 'suggested_coefficients' in ma_suggestions:
        new_coeffs = ma_suggestions['suggested_coefficients']
        print(f"建议系数: {new_coeffs}")
        
        # 验证修改后的模型
        new_result = tsdiag.invertibility_check(new_coeffs)
        print(f"修改后可逆性: {'是' if new_result.is_invertible else '否'}")
    
    # 6. 综合ARMA分析演示
    demo_header("6. 综合ARMA分析演示")
    
    arma_models = [
        {'ar': [0.5], 'ma': [0.3]},
        {'ar': [1.1], 'ma': [0.3]},
        {'ar': [0.5], 'ma': [1.1]},
        {'ar': [0.5, -0.3], 'ma': [0.4, 0.2]}
    ]
    
    arma_names = ["有效ARMA", "AR无效", "MA无效", "复杂ARMA"]
    
    arma_results = tsdiag.batch_model_analysis(arma_models, arma_names)
    
    print(f"{'模型':<12} {'AR平稳':<8} {'MA可逆':<8} {'整体':<8}")
    print("-" * 40)
    
    for result in arma_results:
        if 'error' not in result:
            name = result['model_name']
            ar_ok = "是" if result.get('ar', {}).get('is_stationary', False) else "否"
            ma_ok = "是" if result.get('ma', {}).get('is_invertible', False) else "否"
            overall = "是" if result.get('overall', {}).get('model_valid', False) else "否"
            print(f"{name:<12} {ar_ok:<8} {ma_ok:<8} {overall:<8}")
    
    # 结束
    demo_header("演示完成")
    print("🎉 时间序列模型分析与诊断工具功能演示完成！")
    print("\n📚 更多信息:")
    print("  • 查看 README.md 了解详细文档")
    print("  • 运行 'tsdiag --help' 查看命令行帮助")
    print("  • 运行 'tsdiag examples' 查看更多示例")
    print("  • 查看 examples/ 目录中的其他示例文件")


if __name__ == "__main__":
    main()
