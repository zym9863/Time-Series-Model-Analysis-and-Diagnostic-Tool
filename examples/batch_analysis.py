#!/usr/bin/env python3
"""
时间序列模型分析与诊断工具 - 批量分析示例

本示例展示了如何使用tsdiag库进行批量模型分析和比较。
"""

import tsdiag
import numpy as np


def main():
    print("=" * 60)
    print("时间序列模型分析与诊断工具 - 批量分析示例")
    print("=" * 60)
    
    # 1. 批量AR模型分析
    print("\n1. 批量AR模型平稳性分析")
    print("-" * 40)
    
    ar_models = [
        [0.5],          # 平稳
        [1.1],          # 非平稳
        [0.5, -0.3],    # 平稳
        [1.2, -0.1],    # 非平稳
        [0.8, 0.15],    # 平稳
    ]
    
    model_names = [
        "AR(1)_稳定",
        "AR(1)_不稳定", 
        "AR(2)_稳定",
        "AR(2)_不稳定",
        "AR(2)_边际"
    ]
    
    ar_results = tsdiag.batch_stationarity_check(ar_models, model_names)
    
    print("AR模型批量分析结果:")
    print(f"{'模型名称':<15} {'平稳性':<8} {'稳定性边际':<12} {'风险等级':<8}")
    print("-" * 50)
    
    for result in ar_results:
        if 'error' not in result:
            status = "是" if result['is_stationary'] else "否"
            margin = f"{result['stability_margin']:.3f}"
            risk = result['risk_level']
            print(f"{result['model_name']:<15} {status:<8} {margin:<12} {risk:<8}")
        else:
            print(f"{result['model_name']:<15} 错误: {result['error']}")
    
    # 2. 批量MA模型分析
    print("\n\n2. 批量MA模型可逆性分析")
    print("-" * 40)
    
    ma_models = [
        [0.5],          # 可逆
        [1.1],          # 不可逆
        [0.5, 0.3],     # 可逆
        [1.2, 0.1],     # 不可逆
        [0.8, 0.15],    # 可逆
    ]
    
    ma_model_names = [
        "MA(1)_可逆",
        "MA(1)_不可逆",
        "MA(2)_可逆", 
        "MA(2)_不可逆",
        "MA(2)_边际"
    ]
    
    ma_results = tsdiag.batch_invertibility_check(ma_models, ma_model_names)
    
    print("MA模型批量分析结果:")
    print(f"{'模型名称':<15} {'可逆性':<8} {'可逆性边际':<12} {'风险等级':<8}")
    print("-" * 50)
    
    for result in ma_results:
        if 'error' not in result:
            status = "是" if result['is_invertible'] else "否"
            margin = f"{result['invertibility_margin']:.3f}"
            risk = result['risk_level']
            print(f"{result['model_name']:<15} {status:<8} {margin:<12} {risk:<8}")
        else:
            print(f"{result['model_name']:<15} 错误: {result['error']}")
    
    # 3. MA模型比较
    print("\n\n3. MA模型比较分析")
    print("-" * 40)
    
    comparison = tsdiag.compare_ma_models(ma_models, ma_model_names)
    
    print(f"总模型数: {comparison['total_models']}")
    print(f"可逆模型数: {comparison['invertible_models']}")
    print(f"不可逆模型数: {comparison['non_invertible_models']}")
    print(f"可逆性比率: {comparison['invertibility_rate']:.2%}")
    
    if comparison['best_model']:
        best = comparison['best_model']
        print(f"\n最佳模型: {best['model_name']}")
        print(f"  可逆性边际: {best['invertibility_margin']:.3f}")
        print(f"  风险等级: {best['risk_level']}")
    
    if comparison['worst_model']:
        worst = comparison['worst_model']
        print(f"\n最差模型: {worst['model_name']}")
        print(f"  可逆性边际: {worst['invertibility_margin']:.3f}")
        print(f"  风险等级: {worst['risk_level']}")
    
    # 4. 综合ARMA模型分析
    print("\n\n4. 综合ARMA模型分析")
    print("-" * 40)
    
    arma_models = [
        {'ar': [0.5], 'ma': [0.3]},
        {'ar': [1.1], 'ma': [0.3]},
        {'ar': [0.5], 'ma': [1.1]},
        {'ar': [0.5, -0.3], 'ma': [0.4, 0.2]},
        {'ar': [1.2, -0.1], 'ma': [1.1, 0.1]},
    ]
    
    arma_names = [
        "ARMA(1,1)_有效",
        "ARMA(1,1)_AR无效",
        "ARMA(1,1)_MA无效",
        "ARMA(2,2)_有效",
        "ARMA(2,2)_无效"
    ]
    
    arma_results = tsdiag.batch_model_analysis(arma_models, arma_names)
    
    print("ARMA模型综合分析结果:")
    print(f"{'模型名称':<15} {'AR平稳':<8} {'MA可逆':<8} {'整体有效':<10}")
    print("-" * 50)
    
    for result in arma_results:
        if 'error' not in result:
            ar_status = "是" if result.get('ar', {}).get('is_stationary', False) else "否"
            ma_status = "是" if result.get('ma', {}).get('is_invertible', False) else "否"
            overall_valid = "是" if result.get('overall', {}).get('model_valid', False) else "否"
            print(f"{result['model_name']:<15} {ar_status:<8} {ma_status:<8} {overall_valid:<10}")
        else:
            print(f"{result['model_name']:<15} 错误: {result['error']}")
    
    # 5. 修改建议示例
    print("\n\n5. 模型修改建议")
    print("-" * 40)
    
    problematic_models = [
        ([1.1], "非平稳AR(1)"),
        ([1.2, -0.1], "非平稳AR(2)"),
    ]
    
    for coeffs, description in problematic_models:
        print(f"\n{description}模型: {coeffs}")
        suggestions = tsdiag.suggest_ar_modifications(coeffs)
        
        if suggestions['is_modification_needed']:
            print("修改建议:")
            for suggestion in suggestions['suggestions']:
                print(f"  • {suggestion}")
            
            if 'suggested_coefficients' in suggestions:
                print(f"  建议系数: {suggestions['suggested_coefficients']}")
                
                # 验证建议的系数
                new_result = tsdiag.stationarity_check(suggestions['suggested_coefficients'])
                print(f"  修改后平稳性: {'是' if new_result.is_stationary else '否'}")
        else:
            print("无需修改")


if __name__ == "__main__":
    main()
