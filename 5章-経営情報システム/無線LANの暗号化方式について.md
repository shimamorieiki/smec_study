# 無線LANの暗号化方式について

## 概要
無線LAN（Wi-Fi）は電波を使用してデータ通信を行うため、適切な暗号化を行わないと通信内容が傍受される危険性があります。そのため、無線LANの発展と共に様々な暗号化方式が開発され、セキュリティの向上が図られてきました。本資料では、代表的な無線LAN暗号化方式について、その仕組みや特徴、セキュリティレベルを詳しく解説します。

## 1. 基本概念・仕組み

### 無線LAN暗号化の基本原理
- **定義**: 無線LANで送受信されるデータを暗号化し、第三者による傍受や改ざんから保護する技術
- **動作原理**: 送信側でデータを暗号化し、受信側で復号化することで、電波を傍受されても内容を解読できないようにする
- **特徴**: 
  - 暗号化キーを共有する仕組みが必要
  - 暗号化アルゴリズムの強度がセキュリティレベルを決定
  - 認証機能と組み合わせて使用されることが多い

### 暗号化プロトコルの構成要素
- **暗号化アルゴリズム**: データを暗号化・復号化する数学的手法
- **認証方式**: 接続を許可するデバイスを識別する仕組み
- **鍵管理**: 暗号化キーの生成、配布、更新を管理する仕組み
- **完全性チェック**: データが改ざんされていないことを確認する機能

## 2. 種類・分類

### 暗号化方式の発展経緯
無線LAN暗号化方式は、セキュリティの脆弱性が発見されるたびに、より強固な方式へと進化してきました。

### WEP (Wired Equivalent Privacy)
**特徴:**
- 1997年に策定された最初の無線LAN暗号化規格
- RC4暗号化アルゴリズムを使用
- 40ビットまたは104ビットの固定鍵を使用（実際には24ビットのIVを含めて64/128ビット）
- 静的な共有鍵方式

**算出方法:**
```
暗号化データ = RC4(IV + 共有鍵) XOR 平文データ
IV: 初期化ベクトル（24ビット）
共有鍵: 40ビットまたは104ビット
```

**📊 具体的な計算例**
**例: WEPによる暗号化プロセス**
- 平文データ: "Hello" (48 65 6C 6C 6F)
- 共有鍵: 40ビット (例: A1 B2 C3 D4 E5)
- IV: 24ビット (例: 12 34 56)

**ステップ1: RC4鍵ストリームの生成**
```
RC4入力 = IV + 共有鍵 = 12 34 56 A1 B2 C3 D4 E5
RC4出力（鍵ストリーム） = 7B 4A 5E 42 3C...
```

**ステップ2: XOR演算による暗号化**
```
平文:     48 65 6C 6C 6F
鍵ストリーム: 7B 4A 5E 42 3C
暗号文:   33 2F 32 2E 53
```

**結果: 暗号化されたデータ = 33 2F 32 2E 53**

💡 **実際の現場では**: WEPは現在セキュリティ上の脆弱性から使用が推奨されていません。IVが24ビットと短く、約1万6千個のパケットで重複が発生し、暗号解読が可能になります。

### WPA (Wi-Fi Protected Access)
**特徴:**
- 2003年に策定されたWEPの後継規格
- TKIP（Temporal Key Integrity Protocol）を採用
- 128ビットの動的鍵を使用
- パケットごとに異なる鍵を生成

**算出方法:**
```
一時鍵 = PRF(PMK, "Pairwise key expansion", 
         Min(AA,SA) || Max(AA,SA) || Min(ANonce,SNonce) || Max(ANonce,SNonce))
PMK: Pairwise Master Key
AA: Authenticator Address (APのMACアドレス)
SA: Supplicant Address (クライアントのMACアドレス)
ANonce/SNonce: ランダムな値
```

**📊 具体的な計算例**
**例: WPA-PSKによる鍵生成**
- パスフレーズ: "MyPassword123"
- SSID: "MyNetwork"
- SSID長: 9バイト

**ステップ1: PMKの生成（PBKDF2）**
```
PMK = PBKDF2(パスフレーズ, SSID, 4096, 256)
    = PBKDF2("MyPassword123", "MyNetwork", 4096, 256)
    = 64バイトの16進数値
```

**ステップ2: PTKの生成（4-way handshake）**
```
PTK = PRF-512(PMK, "Pairwise key expansion", 
              AA || SA || ANonce || SNonce)
```

💡 **実際の現場では**: WPAはWEPより安全ですが、TKIPにも脆弱性が発見されており、現在はWPA2以降の使用が推奨されています。

### WPA2 (Wi-Fi Protected Access 2)
**特徴:**
- 2004年に策定された現在の主流規格
- AES-CCMP暗号化を採用
- 128ビットの強力な暗号化
- IEEE 802.11i規格に準拠

**算出方法:**
```
暗号化データ = AES-CCMP(鍵, 平文, AAD)
鍵: 128ビットの暗号化鍵
AAD: Additional Authentication Data
CCMP: Counter Mode with CBC-MAC Protocol
```

**📊 具体的な計算例**
**例: WPA2-Enterpriseでの認証と暗号化**
- 認証サーバー: RADIUSサーバー
- 認証方式: EAP-TLS
- ユーザー証明書: 有効

**ステップ1: EAP認証プロセス**
```
1. クライアント → AP: EAP-Start
2. AP → 認証サーバー: EAP-Identity Request
3. クライアント → 認証サーバー: 証明書交換
4. 認証成功 → PMK生成
```

**ステップ2: AES-CCMP暗号化**
```
Nonce = PN || A2 || Priority
CCMPヘッダー = PN || KeyID
暗号化 = AES-CTR(Key, Nonce, Data)
MIC = AES-CBC-MAC(Key, Nonce, AAD || Data)
```

💡 **実際の現場では**: WPA2は長年にわたり安全とされてきましたが、2017年にKRACK攻撃が発見され、適切なパッチ適用が必要です。

### WPA3 (Wi-Fi Protected Access 3)
**特徴:**
- 2018年に策定された最新規格
- SAE（Simultaneous Authentication of Equals）認証を採用
- 192ビット暗号化モード（Enterprise）をサポート
- 前方秘匿性（Forward Secrecy）を提供

**算出方法:**
```
SAE交換:
1. Commit: 
   scalar = (rand() mod (q-1)) + 1
   element = scalar * P
   
2. Confirm:
   confirm = HMAC(KCK, scalar || element || peer_scalar || peer_element)
   
3. PMK導出:
   PMK = KDF(shared_secret, "SAE KCK and PMK")
```

**📊 具体的な計算例**
**例: WPA3-SAEハンドシェイク**
- パスワード: "SecurePass2024"
- 楕円曲線: P-256

**ステップ1: パスワードからの鍵導出**
```
PWE = Hash-to-Curve("SecurePass2024" || MAC1 || MAC2)
```

**ステップ2: Diffie-Hellman鍵交換**
```
クライアント: 
  private_key = random(256bit)
  public_key = private_key * G
  
アクセスポイント:
  private_key = random(256bit)
  public_key = private_key * G
  
共有秘密 = private_key * peer_public_key
```

💡 **実際の現場では**: WPA3はオフライン辞書攻撃に対する耐性があり、公衆Wi-Fiでも個別暗号化（OWE）が可能です。

### その他の暗号化方式

#### WPA3-Enterprise (192ビットモード)
**特徴:**
- 192ビットの暗号化強度
- CNSA（Commercial National Security Algorithm）Suite準拠
- 政府機関や金融機関向け

**使用アルゴリズム:**
```
認証: EAP-TLS with ECDSA-384
鍵導出: HMAC-SHA-384
暗号化: AES-256-GCM
鍵交換: ECDHE with P-384
```

#### OWE (Opportunistic Wireless Encryption)
**特徴:**
- オープンネットワークでの暗号化
- パスワード不要
- 個別暗号化を提供

**動作:**
```
1. Diffie-Hellman鍵交換（自動）
2. PMK生成
3. 4-way handshake
4. データ暗号化（AES）
```

## 3. 詳細仕様・パラメータ

### 暗号化強度の比較
#### 鍵長と暗号化アルゴリズム
| 方式 | 鍵長 | 暗号化アルゴリズム | IVサイズ | 完全性保護 |
|------|------|-------------------|----------|------------|
| WEP | 40/104ビット | RC4 | 24ビット | CRC-32 |
| WPA | 128ビット | RC4 (TKIP) | 48ビット | Michael |
| WPA2 | 128ビット | AES-CCMP | 48ビット | CBC-MAC |
| WPA3 | 128/192ビット | AES-GCMP | 96ビット | GMAC |

#### 認証方式の詳細
- **Open System**: 認証なし（WEPで使用）
- **Shared Key**: 共有鍵による認証（WEPで使用）
- **WPA-PSK/WPA2-PSK**: 事前共有鍵方式
- **WPA-Enterprise/WPA2-Enterprise**: 802.1X/EAP認証
- **WPA3-SAE**: Simultaneous Authentication of Equals
- **WPA3-Enterprise**: 802.1X with enhanced security

## 4. 実装例・適用事例

### 基本実装（ホームルーターの設定）
```bash
# WPA2-PSK設定例（hostapd.conf）
interface=wlan0
driver=nl80211
ssid=MyHomeNetwork
hw_mode=g
channel=6
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0

# WPA2設定
wpa=2
wpa_passphrase=MySecurePassword123!
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
```

### 応用実装（エンタープライズ環境）
```bash
# WPA2-Enterprise設定例（hostapd.conf）
interface=wlan0
driver=nl80211
ssid=CorporateNetwork
hw_mode=a
channel=36
ieee80211n=1
ieee80211ac=1

# WPA2-Enterprise設定
wpa=2
wpa_key_mgmt=WPA-EAP
wpa_pairwise=CCMP
rsn_pairwise=CCMP
auth_algs=1
ieee8021x=1

# RADIUSサーバー設定
auth_server_addr=192.168.1.10
auth_server_port=1812
auth_server_shared_secret=RadiusSecret123!
```

### WPA3実装例
```bash
# WPA3-SAE設定例（hostapd.conf）
interface=wlan0
driver=nl80211
ssid=ModernNetwork
hw_mode=g
channel=11

# WPA3設定
wpa=2
wpa_key_mgmt=SAE
wpa_passphrase=VerySecurePassword2024!
ieee80211w=2  # PMF必須
sae_groups=19 20 21  # 楕円曲線グループ
sae_require_mfp=1
```

### 実際の適用事例

#### 事例1: 大手製造業A社のWPA2-Enterprise導入
- **課題**: 工場内の無線LAN環境で、従業員の認証管理とデバイス制御が必要
- **適用方法**: 
  - RADIUS認証サーバーとActive Directory連携
  - 証明書ベース認証（EAP-TLS）の実装
  - VLANによるネットワーク分離
- **結果**: 
  - 不正アクセスゼロを達成
  - デバイスごとの細かなアクセス制御を実現
- **効果**: セキュリティインシデントが年間10件から0件に削減

#### 事例2: カフェチェーンB社のWPA3導入
- **課題**: 顧客向け無線LANのセキュリティ向上とユーザビリティの両立
- **適用方法**: 
  - WPA3-SAEによるパスワード認証
  - OWEによるオープンネットワークの暗号化
  - Captive Portalとの連携
- **結果**: 
  - パスワードの定期変更が不要に
  - オフライン攻撃への耐性向上
- **効果**: 顧客満足度が15%向上、セキュリティ関連の問い合わせが80%減少

## 5. メリット・デメリット

### メリット
**1. セキュリティの向上（世代が新しいほど）**
- **理由**: 暗号化アルゴリズムの強化と脆弱性対策の実装
- **効果**: 不正アクセスや盗聴のリスクを大幅に低減
- **具体例**: WPA3では辞書攻撃への耐性が格段に向上

**2. 管理の効率化（Enterprise版）**
- **理由**: 集中認証管理とポリシー適用が可能
- **効果**: 大規模環境でも効率的な運用が可能
- **具体例**: 1000台以上のデバイスも一元管理可能

**3. 前方秘匿性（WPA3）**
- **理由**: 過去の通信が後から解読されるリスクを排除
- **効果**: 長期的なセキュリティ保証
- **具体例**: マスターキーが漏洩しても過去の通信は安全

### デメリット
**1. 互換性の問題**
- **理由**: 古いデバイスが新しい規格に対応していない
- **影響**: デバイスの買い替えや設定の複雑化
- **対策**: 移行期間中は複数の規格を併用

**2. 設定の複雑さ（Enterprise版）**
- **理由**: 認証サーバーや証明書の管理が必要
- **影響**: 初期導入コストと運用負荷の増大
- **対策**: 専門知識を持つ担当者の配置や外部委託

**3. パフォーマンスへの影響**
- **理由**: 暗号化・復号化処理によるオーバーヘッド
- **影響**: 特に古いデバイスで通信速度が低下
- **対策**: ハードウェア暗号化対応機器の使用

## 6. 選択・導入の指針

### 暗号化方式選択の基準
| 観点 | WEP | WPA | WPA2 | WPA3 |
|------|-----|-----|------|------|
| セキュリティ | × | △ | ○ | ◎ |
| 互換性 | ◎ | ○ | ○ | △ |
| 設定難易度 | ◎ | ○ | ○ | △ |
| 推奨度 | × | △ | ○ | ◎ |

### 適用判断フローチャート
1. **新規導入か？** 
   - Yes → WPA3を推奨
   - No → 次の判断へ

2. **全デバイスがWPA3対応か？**
   - Yes → WPA3を採用
   - No → 次の判断へ

3. **セキュリティ重視か？**
   - Yes → WPA2/WPA3混在モード
   - No → WPA2を継続使用（定期的な見直し必須）

4. **エンタープライズ環境か？**
   - Yes → WPA2/3-Enterpriseを推奨
   - No → WPA2/3-PSKで十分

### 環境別推奨設定
#### 家庭用
- **推奨**: WPA2-PSK または WPA3-SAE
- **パスワード**: 20文字以上の複雑なもの
- **SSID**: 機器やメーカー名を含まない

#### 中小企業
- **推奨**: WPA2-PSK（将来的にWPA3移行）
- **追加対策**: MACアドレスフィルタリング、定期的なパスワード変更
- **ネットワーク分離**: ゲスト用と業務用を分離

#### 大企業・公共機関
- **推奨**: WPA2/3-Enterprise
- **認証**: 証明書ベース（EAP-TLS）
- **追加対策**: IDS/IPS、定期的なセキュリティ監査

## 7. 最新動向・今後の展望
- **現在の課題**: 
  - IoTデバイスの急増による管理の複雑化
  - 6GHz帯（Wi-Fi 6E/7）での暗号化要件
  - 量子コンピュータへの耐性
  
- **研究動向**: 
  - ポスト量子暗号の適用検討
  - AI/MLを活用した異常検知
  - ゼロトラストネットワークとの統合
  
- **将来予測**: 
  - 2025年までにWPA3が主流に
  - 証明書ベース認証の簡素化
  - 自動セキュリティ設定の標準化
  
- **関連技術**: 
  - Wi-Fi 6/6E/7での拡張セキュリティ機能
  - Private 5Gとの連携
  - SDNによる動的セキュリティポリシー

## 8. 理解度確認クイズ（4択問題20問）

### 問題1
WEPの暗号化で使用される初期化ベクトル（IV）のサイズは何ビットか？

- A) 16ビット
- B) 24ビット
- C) 32ビット
- D) 48ビット

<details>
<summary>解答</summary>
<strong>正解: B) 24ビット</strong><br>
WEPでは24ビットの初期化ベクトル（IV）を使用します。このIVの短さが、WEPの主要な脆弱性の一つです。24ビットでは約1677万通りの組み合わせしかなく、大量のパケットを収集すると同じIVが再利用される確率が高くなり、統計的な解析により暗号が破られる可能性があります。<br>
<br>
Aが間違いの理由：16ビットは短すぎて、実際のWEP規格では採用されていません<br>
Cが間違いの理由：32ビットはWEPのIVサイズより大きく、正しくありません<br>
Dが間違いの理由：48ビットはWPAのTKIPで使用されるIVサイズです
</details>

### 問題2
WPA2で採用されている暗号化方式はどれか？

- A) RC4-TKIP
- B) AES-CCMP
- C) DES-CBC
- D) AES-TKIP

<details>
<summary>解答</summary>
<strong>正解: B) AES-CCMP</strong><br>
WPA2では、AES（Advanced Encryption Standard）暗号化アルゴリズムとCCMP（Counter Mode with CBC-MAC Protocol）を組み合わせたAES-CCMPが標準的に使用されます。これは128ビットのブロック暗号で、高いセキュリティを提供します。<br>
<br>
Aが間違いの理由：RC4-TKIPはWPAで使用される方式で、WPA2では使用されません<br>
Cが間違いの理由：DES-CBCは無線LAN暗号化では使用されない古い暗号化方式です<br>
Dが間違いの理由：AESとTKIPの組み合わせは存在しません。TKIPはRC4ベースです
</details>

### 問題3
WPA-PSKにおいて、パスフレーズから256ビットのPMK（Pairwise Master Key）を生成する際の反復回数は？

- A) 1024回
- B) 2048回
- C) 4096回
- D) 8192回

<details>
<summary>解答</summary>
<strong>正解: C) 4096回</strong><br>
WPA-PSKでは、PBKDF2（Password-Based Key Derivation Function 2）を使用してパスフレーズからPMKを生成します。この際、4096回の反復処理を行うことで、総当たり攻撃や辞書攻撃に対する耐性を高めています。<br>
<br>
計算式：PMK = PBKDF2(パスフレーズ, SSID, 4096, 256)<br>
<br>
Aが間違いの理由：1024回では攻撃への耐性が不十分です<br>
Bが間違いの理由：2048回は標準より少なく、実際には使用されません<br>
Dが間違いの理由：8192回は標準より多く、不要な処理時間がかかります
</details>

### 問題4
WPA3で新たに採用された認証方式は？

- A) EAP-TLS
- B) PEAP
- C) SAE
- D) LEAP

<details>
<summary>解答</summary>
<strong>正解: C) SAE</strong><br>
WPA3では、SAE（Simultaneous Authentication of Equals）という新しい認証方式が採用されました。SAEはDragonfly鍵交換に基づいており、オフライン辞書攻撃に対する耐性を提供し、前方秘匿性も実現します。<br>
<br>
Aが間違いの理由：EAP-TLSは証明書ベースの認証で、WPA2-Enterpriseでも使用されています<br>
Bが間違いの理由：PEAPはWPA/WPA2-Enterpriseで使用される認証方式です<br>
Dが間違いの理由：LEAPはCisco独自の古い認証方式で、現在は非推奨です
</details>

### 問題5
無線LANの暗号化において「前方秘匿性（Forward Secrecy）」を提供する規格は？

- A) WEP
- B) WPA
- C) WPA2
- D) WPA3

<details>
<summary>解答</summary>
<strong>正解: D) WPA3</strong><br>
前方秘匿性とは、現在の秘密鍵が漏洩しても、過去の通信内容が解読されないという性質です。WPA3のSAE認証では、接続ごとに異なる暗号鍵が生成されるため、仮にある時点の鍵が漏洩しても、それ以前の通信は保護されます。<br>
<br>
Aが間違いの理由：WEPは静的な鍵を使用し、前方秘匿性はありません<br>
Bが間違いの理由：WPAも前方秘匿性を提供しません<br>
Cが間違いの理由：WPA2も標準では前方秘匿性を提供しません
</details>

### 問題6
WEPとWPAの主な違いとして正しいものは？

- A) WEPは動的鍵、WPAは静的鍵を使用
- B) WEPは静的鍵、WPAは動的鍵を使用
- C) 両方とも同じRC4暗号で鍵管理のみ異なる
- D) WEPはAES、WPAはRC4を使用

<details>
<summary>解答</summary>
<strong>正解: B) WEPは静的鍵、WPAは動的鍵を使用</strong><br>
WEPでは事前に設定した固定の鍵を使い続けますが、WPAではTKIP（Temporal Key Integrity Protocol）により、パケットごとに異なる鍵を動的に生成します。これにより、WPAはWEPよりも格段に安全性が向上しています。<br>
<br>
Aが間違いの理由：WEPとWPAの鍵管理方式が逆になっています<br>
Cが間違いの理由：両方ともRC4を使用しますが、鍵管理だけでなく、完全性チェックなども異なります<br>
Dが間違いの理由：WEPもWPAもRC4を使用します。AESを使用するのはWPA2です
</details>

### 問題7
WPA2-Enterpriseで一般的に使用される認証サーバーは？

- A) DNSサーバー
- B) RADIUSサーバー
- C) DHCPサーバー
- D) Webサーバー

<details>
<summary>解答</summary>
<strong>正解: B) RADIUSサーバー</strong><br>
WPA2-Enterpriseでは、IEEE 802.1X認証を使用し、認証サーバーとしてRADIUS（Remote Authentication Dial-In User Service）サーバーが標準的に使用されます。RADIUSサーバーは、ユーザー認証、認可、アカウンティング（AAA）機能を提供します。<br>
<br>
Aが間違いの理由：DNSサーバーは名前解決を行うサーバーで、認証機能はありません<br>
Cが間違いの理由：DHCPサーバーはIPアドレスを配布するサーバーで、認証機能はありません<br>
Dが間違いの理由：Webサーバーは認証ポータルとして使用されることはありますが、802.1X認証サーバーではありません
</details>

### 問題8
TKIPで使用される完全性チェック方式は？

- A) CRC-32
- B) Michael
- C) CBC-MAC
- D) GMAC

<details>
<summary>解答</summary>
<strong>正解: B) Michael</strong><br>
TKIP（Temporal Key Integrity Protocol）では、メッセージの完全性を確認するためにMichaelアルゴリズムを使用します。Michaelは8バイトのMIC（Message Integrity Code）を生成し、データの改ざんを検出します。<br>
<br>
Aが間違いの理由：CRC-32はWEPで使用される完全性チェックで、暗号学的に弱いです<br>
Cが間違いの理由：CBC-MACはWPA2のCCMPで使用されます<br>
Dが間違いの理由：GMACはWPA3のGCMPで使用される方式です
</details>

### 問題9
公衆Wi-Fiで個別暗号化を提供するWPA3の機能は？

- A) PMF (Protected Management Frames)
- B) OWE (Opportunistic Wireless Encryption)
- C) SAE (Simultaneous Authentication of Equals)
- D) MFP (Management Frame Protection)

<details>
<summary>解答</summary>
<strong>正解: B) OWE (Opportunistic Wireless Encryption)</strong><br>
OWEは、パスワードなしのオープンネットワークでも、各クライアントとアクセスポイント間で個別の暗号化を自動的に確立する機能です。Diffie-Hellman鍵交換を使用して、ユーザーの操作なしに暗号化通信を実現します。<br>
<br>
Aが間違いの理由：PMFは管理フレームの保護機能で、個別暗号化とは異なります<br>
Cが間違いの理由：SAEはWPA3の認証方式ですが、パスワードが必要です<br>
Dが間違いの理由：MFPはPMFと同じく管理フレーム保護で、個別暗号化機能ではありません
</details>

### 問題10
WPA3-Enterpriseの192ビットモードで使用される暗号化アルゴリズムは？

- A) AES-128-CCMP
- B) AES-192-CCMP
- C) AES-256-CCMP
- D) AES-256-GCM

<details>
<summary>解答</summary>
<strong>正解: D) AES-256-GCM</strong><br>
WPA3-Enterpriseの192ビットセキュリティモードでは、実際にはAES-256-GCM（Galois/Counter Mode）が使用されます。「192ビットモード」という名称は、全体的なセキュリティ強度を指し、暗号化には256ビットのAESが使用されます。<br>
<br>
Aが間違いの理由：AES-128は通常のWPA2/WPA3で使用される強度です<br>
Bが間違いの理由：AES-192は無線LAN規格では一般的に使用されません<br>
Cが間違いの理由：CCMPではなくGCMが192ビットモードで使用されます
</details>

### 問題11
ある企業でWPA2-PSKを使用している。パスフレーズが「CompanyWiFi2024」、SSIDが「CorpNetwork」の場合、PMK生成に関する説明として正しいものは？

- A) パスフレーズのみを使用してPMKを生成する
- B) SSIDのみを使用してPMKを生成する
- C) パスフレーズとSSIDの両方を使用してPMKを生成する
- D) パスフレーズ、SSID、MACアドレスを使用してPMKを生成する

<details>
<summary>解答</summary>
<strong>正解: C) パスフレーズとSSIDの両方を使用してPMKを生成する</strong><br>
WPA-PSKでは、PBKDF2関数を使用してPMKを生成します。この際、パスフレーズをパスワードとして、SSIDをsaltとして使用します。これにより、同じパスフレーズでも異なるSSIDでは異なるPMKが生成され、レインボーテーブル攻撃への耐性が向上します。<br>
<br>
計算式：PMK = PBKDF2(PassPhrase, SSID, 4096, 256)<br>
実例：PMK = PBKDF2("CompanyWiFi2024", "CorpNetwork", 4096, 256)<br>
<br>
Aが間違いの理由：パスフレーズだけでは不十分で、SSIDも必要です<br>
Bが間違いの理由：SSIDだけではPMKを生成できません<br>
Dが間違いの理由：MACアドレスはPMK生成には使用されません（PTK生成で使用）
</details>

### 問題12
WEPで64ビット暗号化を使用する場合、実際にユーザーが設定する鍵の長さは？

- A) 24ビット（3文字）
- B) 40ビット（5文字）
- C) 64ビット（8文字）
- D) 104ビット（13文字）

<details>
<summary>解答</summary>
<strong>正解: B) 40ビット（5文字）</strong><br>
WEPの「64ビット暗号化」では、24ビットのIV（初期化ベクトル）と40ビットの秘密鍵を組み合わせて64ビットとなります。ユーザーが設定するのは40ビットの秘密鍵部分のみで、これは5文字のASCII文字、または10桁の16進数で表されます。<br>
<br>
計算：64ビット = 24ビット（IV） + 40ビット（秘密鍵）<br>
<br>
Aが間違いの理由：24ビットはIVのサイズで、ユーザーが設定する鍵ではありません<br>
Cが間違いの理由：64ビット全体をユーザーが設定するわけではありません<br>
Dが間違いの理由：104ビットは128ビットWEPで使用される鍵長です
</details>

### 問題13
WPA2の4-way handshakeで生成されるPTK（Pairwise Transient Key）の構成要素として含まれないものは？

- A) KCK (Key Confirmation Key)
- B) KEK (Key Encryption Key)
- C) TK (Temporal Key)
- D) GTK (Group Temporal Key)

<details>
<summary>解答</summary>
<strong>正解: D) GTK (Group Temporal Key)</strong><br>
PTKは個別の通信用の鍵セットで、KCK（鍵確認用）、KEK（鍵暗号化用）、TK（データ暗号化用）の3つで構成されます。GTKはグループ通信（ブロードキャスト/マルチキャスト）用の鍵で、PTKとは別に管理されます。<br>
<br>
PTKの構成：<br>
- KCK: EAPOLフレームのMIC計算用（128ビット）<br>
- KEK: GTKの暗号化配布用（128ビット）<br>
- TK: ユニキャストデータの暗号化用（128ビット）<br>
<br>
Aが間違いの理由：KCKはPTKの重要な構成要素です<br>
Bが間違いの理由：KEKもPTKの構成要素です<br>
Cが間違いの理由：TKはPTKの中核となる暗号化鍵です
</details>

### 問題14
あるカフェでWPA3-SAEを導入した。従来のWPA2-PSKと比較して、ブルートフォース攻撃に対する耐性が向上した理由は？

- A) より長い暗号鍵を使用するため
- B) オンライン攻撃に対してレート制限があるため
- C) 暗号化アルゴリズムがAESからGCMに変更されたため
- D) パスワードの最小長が増加したため

<details>
<summary>解答</summary>
<strong>正解: B) オンライン攻撃に対してレート制限があるため</strong><br>
WPA3-SAEでは、認証試行に失敗した場合、次の試行までに遅延が発生し、連続的な失敗により遅延時間が増加します。これにより、オンラインでのブルートフォース攻撃やビット攻撃が実質的に不可能になります。また、オフライン攻撃も、Dragonfly鍵交換により防御されます。<br>
<br>
【補足】WPA2-PSKでは、4-way handshakeをキャプチャすれば、オフラインで総当たり攻撃が可能でした。<br>
<br>
Aが間違いの理由：暗号鍵の長さは同じ128ビットです<br>
Cが間違いの理由：通常のWPA3でも主にAES-CCMPを使用します<br>
Dが間違いの理由：パスワードの最小長の規定は変更されていません
</details>

### 問題15
企業がWPA2-EnterpriseでEAP-TLSを使用する場合、クライアント側に必要なものは？

- A) ユーザー名とパスワードのみ
- B) 共有秘密鍵のみ
- C) クライアント証明書と秘密鍵
- D) RADIUSサーバーのIPアドレス

<details>
<summary>解答</summary>
<strong>正解: C) クライアント証明書と秘密鍵</strong><br>
EAP-TLS（Extensible Authentication Protocol - Transport Layer Security）は証明書ベースの認証方式で、クライアントはPKI（Public Key Infrastructure）により発行されたクライアント証明書と、それに対応する秘密鍵を保持する必要があります。これにより、相互認証が可能となり、高いセキュリティを実現します。<br>
<br>
実装例：<br>
1. CAがクライアント証明書を発行<br>
2. クライアントに証明書と秘密鍵をインストール<br>
3. 接続時に証明書で認証<br>
<br>
Aが間違いの理由：EAP-TLSは証明書ベースで、パスワード認証ではありません<br>
Bが間違いの理由：共有秘密鍵ではなく、PKIベースの証明書を使用します<br>
Dが間違いの理由：RADIUSサーバーのアドレスはアクセスポイント側の設定です
</details>

### 問題16
ホテルが宿泊客向けWi-Fiのセキュリティを向上させたい。現在はパスワードなしのオープンネットワークを使用している。WPA3を導入する場合、最も適切な構成は？

- A) WPA3-SAEで複雑なパスワードを設定し、チェックイン時に配布
- B) WPA3-Enterpriseを導入し、宿泊客ごとに証明書を発行
- C) WPA3のOWE機能を有効にし、パスワードなしで個別暗号化
- D) WPA3-PSKで日替わりパスワードを設定

<details>
<summary>解答</summary>
<strong>正解: C) WPA3のOWE機能を有効にし、パスワードなしで個別暗号化</strong><br>
OWE（Opportunistic Wireless Encryption）は、オープンネットワークの利便性を保ちながら、各クライアントとアクセスポイント間で自動的に個別の暗号化を確立します。宿泊客はパスワード入力なしで接続でき、かつ通信は暗号化されるため、ホテルのユースケースに最適です。<br>
<br>
実際の動作：<br>
1. 宿泊客がSSIDを選択<br>
2. 自動的にDiffie-Hellman鍵交換実行<br>
3. 個別の暗号鍵で通信を保護<br>
<br>
Aが間違いの理由：パスワード配布の運用負荷が高く、ゲストの利便性が低下します<br>
Bが間違いの理由：証明書発行は非現実的で、運用が複雑すぎます<br>
Dが間違いの理由：日替わりパスワードは管理が煩雑で、深夜の切り替え時に問題が発生します
</details>

### 問題17
製造業の工場で、産業用IoTデバイス（温度センサー、制御機器など）を無線LANに接続する必要がある。これらのデバイスの多くは、WPA3に対応していない。セキュリティを最大化するための推奨構成は？

- A) すべてのデバイスをWEPで統一する
- B) WPA2-PSKを使用し、MACアドレスフィルタリングを併用
- C) WPA2/WPA3混在モードで、可能な限りWPA3を使用
- D) オープンネットワークにして、VPNで保護

<details>
<summary>解答</summary>
<strong>正解: C) WPA2/WPA3混在モードで、可能な限りWPA3を使用</strong><br>
混在モードでは、WPA3対応デバイスはWPA3で、非対応デバイスはWPA2で接続できます。これにより、既存デバイスの互換性を保ちながら、可能な限り高いセキュリティを実現できます。さらに、ネットワークセグメンテーションやVLAN分離を併用することで、リスクを最小化できます。<br>
<br>
推奨される追加対策：<br>
- IoTデバイス専用のVLAN作成<br>
- デバイスごとのアクセス制御<br>
- 定期的なファームウェア更新<br>
- ネットワーク監視の強化<br>
<br>
Aが間違いの理由：WEPは脆弱性が多く、産業環境では絶対に避けるべきです<br>
Bが間違いの理由：MACアドレスは偽装可能で、セキュリティ強化には限界があります<br>
Dが間違いの理由：オープンネットワークは基本的な暗号化もなく、VPN設定も複雑です
</details>

### 問題18
金融機関が新しい支店にWi-Fi環境を構築する。規制要件により、強力な暗号化と監査証跡が必要。最適な構成は？

- A) WPA3-PSKで256文字のランダムパスワード
- B) WPA3-Enterprise 192ビットモード with EAP-TLS
- C) WPA2-Enterpriseで毎日パスワードを変更
- D) WPA3-SAEで各部署ごとに異なるパスワード

<details>
<summary>解答</summary>
<strong>正解: B) WPA3-Enterprise 192ビットモード with EAP-TLS</strong><br>
金融機関では、CNSA（Commercial National Security Algorithm）Suite準拠の192ビットセキュリティモードが適切です。これは、AES-256-GCM暗号化、SHA-384ハッシュ、ECDSA-P384署名を使用し、最高レベルのセキュリティを提供します。EAP-TLSによる証明書認証により、強力な相互認証と監査証跡の記録が可能です。<br>
<br>
構成の詳細：<br>
- 認証: EAP-TLS with ECDSA-384証明書<br>
- 暗号化: AES-256-GCM<br>
- 鍵導出: HMAC-SHA-384<br>
- RADIUSサーバーでの詳細ログ記録<br>
<br>
Aが間違いの理由：PSKでは個人認証や監査証跡が不十分です<br>
Cが間違いの理由：WPA2では192ビットモードが使用できず、要件を満たしません<br>
Dが間違いの理由：SAEも共有鍵方式で、企業認証には不適切です
</details>

### 問題19
小規模な設計事務所で、従業員15名とゲスト用のWi-Fiを分離したい。予算とITリソースが限られている。実装すべき構成は？

- A) 物理的に2つのアクセスポイントを設置
- B) 1つのAPで複数SSID（従業員用WPA2-PSK、ゲスト用オープン）
- C) 1つのAPで複数SSID（両方WPA2-PSK、VLANで分離）
- D) WPA3-Enterpriseで部門ごとに認証

<details>
<summary>解答</summary>
<strong>正解: C) 1つのAPで複数SSID（両方WPA2-PSK、VLANで分離）</strong><br>
小規模事務所では、1台のアクセスポイントで複数SSIDを設定し、VLANでネットワークを分離する方法が最もコスト効率的です。両方のネットワークでWPA2-PSKを使用することで、基本的なセキュリティを確保しつつ、VLANによりネットワーク間のアクセスを制限できます。<br>
<br>
推奨設定：<br>
- 従業員SSID: WPA2-PSK、VLAN 10、社内リソースアクセス可<br>
- ゲストSSID: WPA2-PSK、VLAN 20、インターネットのみアクセス可<br>
- ファイアウォールでVLAN間通信を遮断<br>
- 定期的なパスワード変更（3-6ヶ月）<br>
<br>
Aが間違いの理由：2つのAPは費用が高く、小規模環境では過剰です<br>
Bが間違いの理由：ゲスト用オープンネットワークはセキュリティリスクが高いです<br>
Dが間違いの理由：Enterpriseは小規模環境には複雑すぎ、コストも高いです
</details>

### 問題20
2025年に新規で企業ネットワークを構築する場合、将来性を考慮した無線LANセキュリティの推奨事項として適切でないものは？

- A) WPA3対応機器の選定を優先する
- B) 量子コンピュータ耐性を考慮した追加対策を検討する
- C) WPA2との互換性のため、TKIPを有効にする
- D) Wi-Fi 6E/7のセキュリティ機能を活用する

<details>
<summary>解答</summary>
<strong>正解: C) WPA2との互換性のため、TKIPを有効にする</strong><br>
TKIPは既に非推奨とされており、多くの新しい機器では無効化されています。2025年の新規構築では、最低でもAES-CCMPを使用すべきで、TKIPを有効にすることはセキュリティの低下につながります。WPA2互換性が必要な場合でも、AES-CCMPのみを使用するべきです。<br>
<br>
2025年の推奨構成：<br>
- WPA3必須、WPA2は移行期間のみ許可<br>
- 暗号化はAES-GCM/CCMPのみ<br>
- PMF（Protected Management Frames）必須<br>
- 定期的なセキュリティ評価実施<br>
<br>
Aが間違いの理由：WPA3対応は将来性の観点から必須です<br>
Bが間違いの理由：量子耐性は長期的に重要な検討事項です<br>
Dが間違いの理由：最新規格のセキュリティ機能活用は推奨されます
</details>

## 9. 専門用語集

このスライドで使用された専門用語について、アルファベット順・50音順で解説します。

### アルファベット

**AAD (Additional Authentication Data)**
- **読み方**: エーエーディー
- **意味**: 暗号化されないが認証の対象となるデータ。AES-CCMPやAES-GCMで使用され、データの完全性を保証する
- **関連用語**: AEAD、MIC、MAC

**AES (Advanced Encryption Standard)**
- **読み方**: エーイーエス
- **意味**: アメリカ国立標準技術研究所（NIST）が制定した共通鍵暗号方式。128、192、256ビットの鍵長をサポートし、WPA2以降で使用される
- **関連用語**: CCMP、GCM、暗号化アルゴリズム

**CCMP (Counter Mode with CBC-MAC Protocol)**
- **読み方**: シーシーエムピー
- **意味**: WPA2で使用される暗号化プロトコル。AES暗号化とCBC-MACを組み合わせて、機密性と完全性を提供する
- **関連用語**: AES、WPA2、暗号化プロトコル

**CRC-32 (Cyclic Redundancy Check 32-bit)**
- **読み方**: シーアールシー サンジュウニ
- **意味**: WEPで使用される完全性チェック方式。暗号学的には弱く、改ざん検出には不適切
- **関連用語**: ICV、完全性チェック、WEP

**EAP (Extensible Authentication Protocol)**
- **読み方**: イーエーピー
- **意味**: 802.1X認証で使用される拡張可能な認証プロトコル。様々な認証方式（EAP-TLS、PEAP、EAP-TTLSなど）をサポート
- **関連用語**: 802.1X、RADIUS、認証

**GCM (Galois/Counter Mode)**
- **読み方**: ジーシーエム
- **意味**: WPA3で使用される認証付き暗号化モード。AESと組み合わせて使用され、高速な暗号化と認証を提供
- **関連用語**: AES、GMAC、WPA3

**GTK (Group Temporal Key)**
- **読み方**: ジーティーケー
- **意味**: ブロードキャストやマルチキャスト通信の暗号化に使用されるグループ鍵
- **関連用語**: PTK、鍵管理、グループ通信

**IV (Initialization Vector)**
- **読み方**: アイブイ、初期化ベクトル
- **意味**: 暗号化の際に使用されるランダムな値。同じ平文でも異なる暗号文を生成するために使用
- **関連用語**: 暗号化、WEP、ランダム性

**MIC (Message Integrity Code)**
- **読み方**: ミック
- **意味**: メッセージの完全性を確認するためのコード。改ざんされていないことを保証する
- **関連用語**: Michael、完全性、TKIP

**OWE (Opportunistic Wireless Encryption)**
- **読み方**: オーダブリューイー
- **意味**: WPA3で導入された、パスワードなしでも暗号化を提供する機能。公衆Wi-Fiなどで使用
- **関連用語**: WPA3、公衆Wi-Fi、個別暗号化

**PBKDF2 (Password-Based Key Derivation Function 2)**
- **読み方**: ピービーケーディーエフ ツー
- **意味**: パスワードから暗号鍵を生成する関数。WPA-PSKでPMKを生成する際に使用
- **関連用語**: 鍵導出、PMK、WPA-PSK

**PMF (Protected Management Frames)**
- **読み方**: ピーエムエフ
- **意味**: 管理フレームを暗号化・認証する機能。偽装APやDoS攻撃から保護
- **関連用語**: 802.11w、管理フレーム、セキュリティ

**PMK (Pairwise Master Key)**
- **読み方**: ピーエムケー
- **意味**: WPAで使用される256ビットのマスター鍵。PSKモードではパスフレーズから生成、Enterpriseモードでは認証後に生成
- **関連用語**: PTK、鍵階層、WPA

**PSK (Pre-Shared Key)**
- **読み方**: ピーエスケー、事前共有鍵
- **意味**: アクセスポイントとクライアントで事前に共有する鍵。家庭用や小規模環境で使用
- **関連用語**: パスフレーズ、WPA-PSK、共有鍵

**PTK (Pairwise Transient Key)**
- **読み方**: ピーティーケー
- **意味**: 各クライアントとの個別通信用に生成される一時的な鍵セット。KCK、KEK、TKで構成
- **関連用語**: 4-way handshake、PMK、鍵階層

**RADIUS (Remote Authentication Dial-In User Service)**
- **読み方**: ラディウス
- **意味**: ネットワーク認証、認可、アカウンティング（AAA）を提供するプロトコル。Enterpriseモードで使用
- **関連用語**: 802.1X、AAA、認証サーバー

**RC4 (Rivest Cipher 4)**
- **読み方**: アールシー フォー
- **意味**: WEPとWPA（TKIP）で使用されるストリーム暗号。現在は脆弱性により非推奨
- **関連用語**: ストリーム暗号、WEP、TKIP

**SAE (Simultaneous Authentication of Equals)**
- **読み方**: エスエーイー
- **意味**: WPA3で採用された認証方式。Dragonfly鍵交換を使用し、オフライン攻撃への耐性を提供
- **関連用語**: WPA3、Dragonfly、認証

**SSID (Service Set Identifier)**
- **読み方**: エスエスアイディー
- **意味**: 無線LANネットワークを識別する名前。最大32文字
- **関連用語**: ネットワーク名、ビーコン、識別子

**TKIP (Temporal Key Integrity Protocol)**
- **読み方**: ティーキップ
- **意味**: WPAで使用される暗号化プロトコル。WEPの脆弱性を改善したが、現在は非推奨
- **関連用語**: WPA、RC4、動的鍵

**WEP (Wired Equivalent Privacy)**
- **読み方**: ウェップ
- **意味**: 最初の無線LAN暗号化規格。重大な脆弱性があり、現在は使用禁止
- **関連用語**: RC4、静的鍵、暗号化

**WPA (Wi-Fi Protected Access)**
- **読み方**: ダブリューピーエー
- **意味**: WEPの後継として開発された暗号化規格。TKIPを使用
- **関連用語**: TKIP、動的鍵、暗号化規格

**WPA2 (Wi-Fi Protected Access 2)**
- **読み方**: ダブリューピーエー ツー
- **意味**: 現在主流の無線LAN暗号化規格。AES-CCMPを使用
- **関連用語**: AES、CCMP、802.11i

**WPA3 (Wi-Fi Protected Access 3)**
- **読み方**: ダブリューピーエー スリー
- **意味**: 最新の無線LAN暗号化規格。SAE認証やOWEなど新機能を搭載
- **関連用語**: SAE、OWE、前方秘匿性

### あ行

**暗号化アルゴリズム（あんごうかアルゴリズム）**
- **意味**: データを暗号化・復号化するための数学的な手順。AES、RC4などがある
- **関連用語**: 暗号化、復号化、アルゴリズム

**暗号鍵（あんごうかぎ）**
- **意味**: データの暗号化・復号化に使用される秘密の値。鍵長が長いほど一般的に安全
- **関連用語**: 鍵長、鍵管理、暗号化

**一時鍵（いちじかぎ）**
- **意味**: セッションごとまたはパケットごとに生成される短期間のみ有効な鍵
- **関連用語**: PTK、動的鍵、セッション鍵

### か行

**完全性チェック（かんぜんせいチェック）**
- **意味**: データが改ざんされていないことを確認する仕組み。MICやMACを使用
- **関連用語**: MIC、MAC、改ざん検出

**鍵交換（かぎこうかん）**
- **意味**: 通信相手と安全に暗号鍵を共有する手順。Diffie-Hellmanなどの方式がある
- **関連用語**: Diffie-Hellman、鍵配送、鍵共有

**鍵導出関数（かぎどうしゅつかんすう）**
- **意味**: パスワードやマスター鍵から、実際に使用する暗号鍵を生成する関数
- **関連用語**: PBKDF2、KDF、鍵生成

**共有鍵暗号（きょうゆうかぎあんごう）**
- **意味**: 暗号化と復号化に同じ鍵を使用する暗号方式。対称鍵暗号とも呼ばれる
- **関連用語**: 対称鍵暗号、AES、秘密鍵

### さ行

**事前共有鍵（じぜんきょうゆうかぎ）**
- **意味**: 通信開始前に、送信者と受信者で共有しておく秘密鍵。PSKとも呼ばれる
- **関連用語**: PSK、パスフレーズ、共有秘密

**証明書認証（しょうめいしょにんしょう）**
- **意味**: デジタル証明書を使用して相手の正当性を確認する認証方式
- **関連用語**: PKI、EAP-TLS、デジタル証明書

**ストリーム暗号（ストリームあんごう）**
- **意味**: データを1ビットまたは1バイト単位で暗号化する方式。RC4が代表例
- **関連用語**: RC4、ブロック暗号、暗号方式

### た行

**対称鍵暗号（たいしょうかぎあんごう）**
- **意味**: 暗号化と復号化に同じ鍵を使用する暗号方式。共有鍵暗号とも呼ばれる
- **関連用語**: 共有鍵暗号、AES、DES

**動的鍵（どうてきかぎ）**
- **意味**: 通信中に定期的または必要に応じて変更される暗号鍵
- **関連用語**: 静的鍵、TKIP、鍵更新

### な行

**認証サーバー（にんしょうサーバー）**
- **意味**: ユーザーやデバイスの認証を行うサーバー。RADIUSサーバーが一般的
- **関連用語**: RADIUS、認証、AAA

### は行

**パスフレーズ（パスフレーズ）**
- **意味**: WPA-PSKで使用される、8〜63文字の文字列。これからPMKが生成される
- **関連用語**: PSK、PMK、パスワード

**ハンドシェイク（ハンドシェイク）**
- **意味**: 通信開始時に行われる、接続確立や鍵交換のための一連の手順
- **関連用語**: 4-way handshake、認証、鍵交換

**ブロック暗号（ブロックあんごう）**
- **意味**: データを固定長のブロック単位で暗号化する方式。AESが代表例
- **関連用語**: AES、ストリーム暗号、暗号方式

### ま行

**前方秘匿性（ぜんぽうひとくせい）**
- **意味**: 現在の鍵が漏洩しても、過去の通信内容が解読されない性質
- **関連用語**: Forward Secrecy、WPA3、セキュリティ属性

### ら行

**乱数生成（らんすうせいせい）**
- **意味**: 予測不可能な数値を生成すること。暗号化において重要な要素
- **関連用語**: エントロピー、IV、Nonce

---

**専門用語集作成時の注意点:**
- **技術的正確性**: 技術定義は業界標準に準拠
- **実装観点**: 実際の開発で使われる文脈も含めて説明
- **英語併記**: 原語がある場合は英語も併記
- **関連技術との関係**: 他の技術や概念との関係も明記