# On the Links Public Claim-to-Evidence Evaluation OS

株式会社オンザリンクスの**公開理念と公開行動の整合性**を、固定した調査義務、Source-boundなEvidence区間、複数の評価条件、Hash binding、Certificate Semantic Replayによって検証する公開リポジトリです。

## 結論

- Decision: **ROBUST / PUBLIC_ALIGNMENT_ESTABLISHED**
- Score Envelope: **70.0–88.6875**
- Strict Establishment Line: **68.0**
- Guaranteed Lower Bound: **70.0**
- Evaluation Families: **60**
- Investigation Gate: **32 / 32 CLOSED**

これは「オンザリンクスは70点の会社」という意味ではありません。公開Evidenceの解釈、Criterionの重み、判定閾値及び区間内の不確実性を、宣言した範囲で変えても、**公開理念―行動整合性の成立が反転しない**という結果です。

## 評価者との関係

評価実施者の株式会社GhostDrift数理研究所は、オンザリンクスの**戦略的パートナー・共同AIアシュアランス実装当事者**です。本評価は独立第三者監査ではありません。

その関係を隠さず、信頼の根拠を「評価者の中立性」ではなく、次に置いています。

1. 人間が設定したEvidence区間を、Source・説明・独立性区分・限界とともに公開する
2. 固定評価宇宙をHashへ結合し、入力差し替えを検出する
3. 会社非統制情報と重大反証候補の調査Gateを通過しなければ数値評価を確定しない
4. 入力固定後の全Mapping・Weight・Threshold・Reference・区間完備化を横断する
5. Certificateから調査Gateと数値計算を完全再計算できる

## Evidence区間について

Evidence区間は機械が自動生成した「客観点」ではありません。公開Sourceを読み、コード内のDimension Anchorに照らして人間が設定した**0〜4の整数序数区間**です。

Evaluation OSは各区間が唯一の正解であるとは主張しません。一方、Sourceのない区間、限界説明のない区間、非整数境界を拒否し、区間を変更した場合はFixed Evaluation Universe HashとCertificateが変わり、全評価Familyの再実行を要求します。

## 公開成果物

公開成果物は3点に限定しています。

| ファイル | 役割 |
|---|---|
| `①評価OS評価レポートまとめ（オンザリンクス社）.html` | 一般向けサマリー／GitHub Pagesのトップページ |
| `②評価OS詳細レポート（オンザリンクス社）.md` | 評価方法、Evidence、結果、関係性、保証境界の正本 |
| `③評価OS実施コード（オンザリンクス社）.py` | Evaluation OS 1.2.0-final実装、証明書生成、Semantic Replay |

リポジトリ運用用の追加物も、`README.md`、`.gitignore`、1つのGitHub Actions workflowだけです。Certificate JSONや重複レポートはコミットしません。

## ローカルで再検証

Python 3.11+、標準ライブラリのみで動作します。

```bash
python -S "③評価OS実施コード（オンザリンクス社）.py" evaluate
python -S "③評価OS実施コード（オンザリンクス社）.py" self-test
python -S "③評価OS実施コード（オンザリンクス社）.py" certificate > certificate.json
python -S "③評価OS実施コード（オンザリンクス社）.py" verify certificate.json
python -S "③評価OS実施コード（オンザリンクス社）.py" freeze
```

## CIで機械検証する内容

`.github/workflows/verify-and-pages.yml` は、`main`へのpush、Pull Request、手動実行で次を検査します。

- 内蔵self-test **23件**
- Certificateを2回生成したbyte列の完全一致
- Certificate Payload HashとSemantic Replay
- Engine Version、Schema、Python code SHA-256
- Fixed Evaluation Universe / Investigation Template / Source Register / Review Records / Prospective CharterのHash
- 60 Family、保証下限70、Strict 68通過、調査Gate 32/32等の主要結果
- 評価者との関係及び「独立第三者監査ではない」という機械可読な開示
- Evidence区間がhuman-authored / source-bound / integer 0–4であるというPolicy
- MarkdownとHTMLに表示したHash・Version・開示の一致

検証成功時だけ、HTML、詳細レポート、実施コード、CI生成Certificate、SHA-256一覧をGitHub Pages用Artifactへまとめます。

## 最短の公開手順

GitHubで空のPublic repositoryを作り、このZIP内の `onzalinx-evaluation-os` フォルダ全体（合計6ファイル）をそのままpushします。

```bash
git init
git add .
git commit -m "Publish On the Links Evaluation OS 1.2"
git branch -M main
git remote add origin <YOUR_REPOSITORY_URL>
git push -u origin main
```

## GitHub Pages

リポジトリ作成後、**Settings → Pages → Build and deployment → Source** を **GitHub Actions** に設定してください。`main`へのpushで、機械検証に成功した場合だけHTMLサマリーを公開します。

## 推奨保護設定

`main`をRuleset又はbranch protectionで保護し、Pull Request経由かつ `Machine verification` 成功をmerge条件にしてください。これにより、コード、レポート又は表示結果だけを単独で書き換えた変更はmainへ入りません。

## Assurance boundary

本評価は `RETROSPECTIVE_TRANSPARENT_PILOT` です。次は保証しません。

- 各Evidence区間が唯一の正解であること
- 独立第三者監査又は評価者の中立性
- 公開情報そのものの真実性
- Web全体、非公開情報、削除済み情報の絶対的網羅
- ProspectiveなTemporal Blind Commitment
- 外部タイムスタンプ、署名者同一性、非否認
- 全顧客での成果、ROI、内製化、職場環境又は商用規模普及

## License

このリポジトリには意図的にOSSライセンスを付与していません。公開閲覧・再検証と、再利用・改変・商用利用の許諾は別です。再利用条件を付与する場合だけ、目的に合うLICENSEを追加してください。
