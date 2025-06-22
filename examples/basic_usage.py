#!/usr/bin/env python3
"""
时间序列模型分析与诊断工具 - 基本使用示例

本示例展示了如何使用tsdiag库进行基本的AR和MA模型检验。
"""

import tsdiag
import numpy as np


def main():
    print("=" * 60)
    print("时间序列模型分析与诊断工具 - 基本使用示例")
    print("=" * 60)
    
    # 1. AR模型平稳性检验
    print("\n1. AR模型平稳性检验")
    print("-" * 30)
    
    # 平稳的AR(1)模型
    print("检验平稳的AR(1)模型: X_t = 0.5*X_{t-1} + ε_t")
    ar_result1 = tsdiag.stationarity_check([0.5])
    print(f"结果: {'平稳' if ar_result1.is_stationary else '非平稳'}")
    print(f"特征根模长: {ar_result1.roots[0].magnitude:.3f}")
    
    # 非平稳的AR(1)模型
    print("\n检验非平稳的AR(1)模型: X_t = 1.1*X_{t-1} + ε_t")
    ar_result2 = tsdiag.stationarity_check([1.1])
    print(f"结果: {'平稳' if ar_result2.is_stationary else '非平稳'}")
    print(f"特征根模长: {ar_result2.roots[0].magnitude:.3f}")
    
    # AR(2)模型
    print("\n检验AR(2)模型: X_t = 0.5*X_{t-1} - 0.06*X_{t-2} + ε_t")
    ar_result3 = tsdiag.stationarity_check([0.5, -0.06])
    print(f"结果: {'平稳' if ar_result3.is_stationary else '非平稳'}")
    print(f"特征根模长: {[root.magnitude for root in ar_result3.roots]}")
    
    # 2. MA模型可逆性检验
    print("\n\n2. MA模型可逆性检验")
    print("-" * 30)
    
    # 可逆的MA(1)模型
    print("检验可逆的MA(1)模型: X_t = ε_t + 0.5*ε_{t-1}")
    ma_result1 = tsdiag.invertibility_check([0.5])
    print(f"结果: {'可逆' if ma_result1.is_invertible else '不可逆'}")
    print(f"特征根模长: {ma_result1.roots[0].magnitude:.3f}")
    
    # 不可逆的MA(1)模型
    print("\n检验不可逆的MA(1)模型: X_t = ε_t + 1.1*ε_{t-1}")
    ma_result2 = tsdiag.invertibility_check([1.1])
    print(f"结果: {'可逆' if ma_result2.is_invertible else '不可逆'}")
    print(f"特征根模长: {ma_result2.roots[0].magnitude:.3f}")
    
    # MA(2)模型
    print("\n检验MA(2)模型: X_t = ε_t + 0.5*ε_{t-1} + 0.06*ε_{t-2}")
    ma_result3 = tsdiag.invertibility_check([0.5, 0.06])
    print(f"结果: {'可逆' if ma_result3.is_invertible else '不可逆'}")
    print(f"特征根模长: {[root.magnitude for root in ma_result3.roots]}")
    
    # 3. 使用高级API
    print("\n\n3. 使用高级API")
    print("-" * 30)
    
    diagnostic = tsdiag.TSModelDiagnostic()
    
    # 检验ARMA模型
    print("检验ARMA(2,2)模型")
    ar_result, ma_result = diagnostic.check_arma_model(
        ar_coefficients=[0.5, -0.3],
        ma_coefficients=[0.4, 0.2],
        verbose=False
    )
    
    summary = diagnostic.get_summary()
    print(f"AR部分平稳: {summary['ar_stationary']}")
    print(f"MA部分可逆: {summary['ma_invertible']}")
    print(f"ARMA模型有效: {summary['arma_valid']}")
    
    # 4. 快速检验
    print("\n\n4. 快速检验（只返回布尔值）")
    print("-" * 30)
    
    models_to_test = [
        ([0.5], "AR(1): φ=0.5"),
        ([1.1], "AR(1): φ=1.1"),
        ([0.5, -0.3], "AR(2): φ₁=0.5, φ₂=-0.3"),
    ]
    
    for coeffs, description in models_to_test:
        is_stationary = tsdiag.quick_ar_check(coeffs)
        print(f"{description}: {'平稳' if is_stationary else '非平稳'}")
    
    # 5. 稳定性分析
    print("\n\n5. 稳定性边际分析")
    print("-" * 30)
    
    test_models = [
        [0.5],      # 稳定
        [0.95],     # 边际稳定
        [1.05],     # 不稳定
    ]
    
    for i, coeffs in enumerate(test_models, 1):
        analysis = tsdiag.analyze_model_stability(ar_coefficients=coeffs)
        ar_info = analysis['ar']
        print(f"模型{i} {coeffs}:")
        print(f"  平稳性: {'是' if ar_info['is_stationary'] else '否'}")
        print(f"  稳定性边际: {ar_info['stability_margin']:.3f}")
        print(f"  风险等级: {ar_info['risk_level']}")


if __name__ == "__main__":
    main()
