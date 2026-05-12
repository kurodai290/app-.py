<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>剣道初段 学科対策（静岡県版）</title>
    <style>
        body { font-family: sans-serif; text-align: center; padding: 20px; background: #f4f4f4; }
        .card { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); max-width: 500px; margin: 20px auto; min-height: 150px; display: flex; align-items: center; justify-content: center; font-size: 1.2rem; font-weight: bold; }
        button { background: #007bff; color: white; border: none; padding: 12px 25px; border-radius: 5px; cursor: pointer; font-size: 1rem; }
        button:hover { background: #0056b3; }
    </style>
</head>
<body>
    <h1>剣道初段 学科対策</h1>
    <p>静岡県 昇段審査用</p>
    <div class="card" id="question">「次へ」を押すと問題が出ます</div>
    <button onclick="nextQuestion()">次の問題を表示</button>

    <script>
        const questions = [
            "「剣道修練の心構え」の全文を書きなさい。",
            "「中段の構え」の作り方と留意点について述べなさい。",
            "「足さばき」の種類を4つ挙げ、説明しなさい。",
            "「間合い」の3つの種類（一足一刀・遠間・近間）について説明しなさい。",
            "「切り返し」を行う目的を3つ以上挙げなさい。",
            "「残心」について説明しなさい。",
            "「竹刀の点検」で確認すべき箇所を具体的に書きなさい。",
            "「剣道を志した理由」を自分の言葉で書きなさい（150〜300字程度）。"
        ];

        function nextQuestion() {
            const q = questions[Math.floor(Math.random() * questions.length)];
            document.getElementById('question').innerText = q;
        }
    </script>
</body>
</html>
