"""
时间序列模型分析与诊断工具FastAPI服务的客户端示例

展示如何使用API进行各种分析。
"""

import requests
import json
from typing import List, Dict, Any


class TSModelAPIClient:
    """时间序列模型分析API客户端"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict[str, Any]:
        """健康检查"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def check_ar_stationarity(self, coefficients: List[float], verbose: bool = False) -> Dict[str, Any]:
        """检验AR模型平稳性"""
        data = {
            "coefficients": coefficients,
            "verbose": verbose
        }
        response = self.session.post(f"{self.base_url}/api/v1/ar/check", json=data)
        response.raise_for_status()
        return response.json()
    
    def check_ma_invertibility(self, coefficients: List[float], verbose: bool = False) -> Dict[str, Any]:
        """检验MA模型可逆性"""
        data = {
            "coefficients": coefficients,
            "verbose": verbose
        }
        response = self.session.post(f"{self.base_url}/api/v1/ma/check", json=data)
        response.raise_for_status()
        return response.json()
    
    def check_arma_model(self, ar_coefficients: List[float], ma_coefficients: List[float], verbose: bool = False) -> Dict[str, Any]:
        """检验ARMA模型"""
        data = {
            "ar_coefficients": ar_coefficients,
            "ma_coefficients": ma_coefficients,
            "verbose": verbose
        }
        response = self.session.post(f"{self.base_url}/api/v1/arma/check", json=data)
        response.raise_for_status()
        return response.json()
    
    def quick_ar_check(self, coefficients: List[float]) -> bool:
        """快速AR检验"""
        data = {"coefficients": coefficients}
        response = self.session.post(f"{self.base_url}/api/v1/ar/quick", json=data)
        response.raise_for_status()
        return response.json()["result"]
    
    def quick_ma_check(self, coefficients: List[float]) -> bool:
        """快速MA检验"""
        data = {"coefficients": coefficients}
        response = self.session.post(f"{self.base_url}/api/v1/ma/quick", json=data)
        response.raise_for_status()
        return response.json()["result"]
    
    def quick_arma_check(self, ar_coefficients: List[float], ma_coefficients: List[float]) -> Dict[str, bool]:
        """快速ARMA检验"""
        data = {
            "ar_coefficients": ar_coefficients,
            "ma_coefficients": ma_coefficients
        }
        response = self.session.post(f"{self.base_url}/api/v1/arma/quick", json=data)
        response.raise_for_status()
        result = response.json()
        return {
            "ar_stationary": result["ar_stationary"],
            "ma_invertible": result["ma_invertible"],
            "overall_valid": result["overall_valid"]
        }
    
    def analyze_stability(self, ar_coefficients: List[float], ma_coefficients: List[float]) -> Dict[str, Any]:
        """稳定性分析"""
        data = {
            "ar_coefficients": ar_coefficients,
            "ma_coefficients": ma_coefficients
        }
        response = self.session.post(f"{self.base_url}/api/v1/stability/analyze", json=data)
        response.raise_for_status()
        return response.json()["analysis"]
    
    def batch_analyze(self, models: List[Dict[str, List[float]]], model_names: List[str] = None) -> Dict[str, Any]:
        """批量分析"""
        data = {
            "models": models,
            "model_names": model_names
        }
        response = self.session.post(f"{self.base_url}/api/v1/batch/analyze", json=data)
        response.raise_for_status()
        return response.json()


def demo_basic_usage():
    """基本使用示例"""
    print("=== 基本使用示例 ===")
    
    client = TSModelAPIClient()
    
    # 健康检查
    print("健康检查:", client.health_check())
    
    # AR模型检验
    ar_coeffs = [0.5, 0.3]
    print(f"\nAR({len(ar_coeffs)})模型系数: {ar_coeffs}")
    ar_result = client.check_ar_stationarity(ar_coeffs, verbose=True)
    print(f"平稳性: {ar_result['is_stationary']}")
    print(f"消息: {ar_result['message']}")
    
    # MA模型检验
    ma_coeffs = [0.4, 0.2]
    print(f"\nMA({len(ma_coeffs)})模型系数: {ma_coeffs}")
    ma_result = client.check_ma_invertibility(ma_coeffs, verbose=True)
    print(f"可逆性: {ma_result['is_invertible']}")
    print(f"消息: {ma_result['message']}")
    
    # ARMA模型检验
    print(f"\nARMA({len(ar_coeffs)},{len(ma_coeffs)})模型")
    arma_result = client.check_arma_model(ar_coeffs, ma_coeffs, verbose=True)
    print(f"整体有效性: {arma_result['overall_valid']}")


def demo_quick_checks():
    """快速检验示例"""
    print("\n=== 快速检验示例 ===")
    
    client = TSModelAPIClient()
    
    # 多个模型的快速检验
    test_models = [
        {"ar": [0.5, 0.3], "ma": [0.4, 0.2]},
        {"ar": [1.2, -0.3], "ma": [0.6, 0.1]},  # 非平稳
        {"ar": [0.1], "ma": [1.5]},  # 非可逆
    ]
    
    for i, model in enumerate(test_models, 1):
        print(f"\n模型 {i}: AR={model['ar']}, MA={model['ma']}")
        result = client.quick_arma_check(model["ar"], model["ma"])
        print(f"  AR平稳: {result['ar_stationary']}")
        print(f"  MA可逆: {result['ma_invertible']}")
        print(f"  整体有效: {result['overall_valid']}")


def demo_stability_analysis():
    """稳定性分析示例"""
    print("\n=== 稳定性分析示例 ===")
    
    client = TSModelAPIClient()
    
    # 接近边界的模型
    ar_coeffs = [0.9, 0.09]  # 接近非平稳
    ma_coeffs = [0.8, 0.15]  # 接近非可逆
    
    print(f"分析模型: AR={ar_coeffs}, MA={ma_coeffs}")
    analysis = client.analyze_stability(ar_coeffs, ma_coeffs)
    
    if 'ar' in analysis:
        ar_info = analysis['ar']
        print(f"\nAR部分:")
        print(f"  平稳性: {ar_info['is_stationary']}")
        print(f"  稳定性边际: {ar_info['stability_margin']:.6f}")
        print(f"  风险级别: {ar_info['risk_level']}")
        if ar_info['suggestions']:
            print(f"  建议: {ar_info['suggestions']}")
    
    if 'ma' in analysis:
        ma_info = analysis['ma']
        print(f"\nMA部分:")
        print(f"  可逆性: {ma_info['is_invertible']}")
        print(f"  可逆性边际: {ma_info['invertibility_margin']:.6f}")
        print(f"  风险级别: {ma_info['risk_level']}")
        if ma_info['suggestions']:
            print(f"  建议: {ma_info['suggestions']}")
    
    if 'overall' in analysis:
        overall = analysis['overall']
        print(f"\n整体评估:")
        print(f"  模型有效: {overall['model_valid']}")
        print(f"  最小稳定性边际: {overall['min_stability_margin']:.6f}")
        print(f"  最大风险级别: {overall['max_risk_level']}")


def demo_batch_analysis():
    """批量分析示例"""
    print("\n=== 批量分析示例 ===")
    
    client = TSModelAPIClient()
    
    # 多个模型的批量分析
    models = [
        {"ar": [0.5, 0.3], "ma": [0.4, 0.2]},
        {"ar": [0.8], "ma": [0.6, 0.1]},
        {"ar": [1.1, -0.2]},  # 只有AR部分，非平稳
        {"ma": [0.9, 0.8]},   # 只有MA部分，非可逆
        {"ar": [0.2, 0.1], "ma": [0.3]},
    ]
    
    model_names = ["ARMA(2,2)", "ARMA(1,2)", "AR(2)", "MA(2)", "ARMA(2,1)"]
    
    print(f"批量分析 {len(models)} 个模型...")
    result = client.batch_analyze(models, model_names)
    
    print(f"\n摘要信息:")
    summary = result['summary']
    print(f"  总模型数: {summary['total_models']}")
    print(f"  有效模型数: {summary['valid_models']}")
    print(f"  错误模型数: {summary['error_models']}")
    print(f"  AR平稳模型数: {summary['ar_stationary_count']}")
    print(f"  MA可逆模型数: {summary['ma_invertible_count']}")
    
    print(f"\n详细结果:")
    for result_item in result['results']:
        if 'error' in result_item:
            print(f"  {result_item['model_name']}: 错误 - {result_item['error']}")
        else:
            name = result_item['model_name']
            valid = result_item.get('overall', {}).get('model_valid', 'N/A')
            print(f"  {name}: 有效性 = {valid}")


def main():
    """主函数"""
    try:
        demo_basic_usage()
        demo_quick_checks()
        demo_stability_analysis()
        demo_batch_analysis()
        
        print("\n=== 所有示例执行完成 ===")
        print("API文档地址: http://localhost:8000/docs")
        print("ReDoc文档地址: http://localhost:8000/redoc")
        
    except requests.exceptions.ConnectionError:
        print("❌ 无法连接到API服务，请确保服务正在运行:")
        print("   python app.py")
        print("   或者: uv run python app.py")
    except Exception as e:
        print(f"❌ 发生错误: {e}")


if __name__ == "__main__":
    main()
