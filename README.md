# LDC-Triad-Core

**Minimal composable Triad** for Latent Dynamics Core (LDC).

CUBEから忠実に抽出した力学単位（LatentSite, InteractionWire, ForceRule, MemoryRule, StateIntegrator）で構成。

## 特徴
- 最小単位で交換可能（ablation実験向き）
- 張力・残差・パルセーションによる創発的安定不安定性
- Triadで3体干渉・役割分化の基礎

## インストール & 実行
```bash
git clone https://github.com/kishimoto-void/ldc-triad-core.git
cd ldc-triad-core
python -m pip install numpy
python example.py
```

## 次のステップ
wCUBE拡張、感情炉、役割分化Cartridgeなど追加可能。

実験は忠実に実際行って。