function initializeChart() {
    var sentences = {{ patient.text_contents | tojson }};
    var sentiScores = {{ patient.senti_scores | tojson }};
    var sentiMagnitudes = {{ patient.senti_magnitudes | tojson }};
    var overallScore = {{ patient.doc_sentiment_score | tojson }};
    var overallMagnitude = {{ patient.doc_sentiment_magnitude | tojson }};

    var overallScoreList = new Array(sentiScores.length).fill(overallScore);
    var overallMagnitudeList = new Array(sentiScores.length).fill(overallMagnitude);

    var labels = [];
    for (var i = 1; i <= sentences.length; i++) {
        labels.push("text" + i);
    }

    const data = {
        labels: labels,
        datasets: [
            {
                label: 'sentiment scores',
                backgroundColor: 'rgb(000, 153, 255)',
                borderColor: 'rgb(000, 153, 255)',
                data: sentiScores,
            },
            {
                label: 'sentiment magnitudes',
                backgroundColor: 'rgb(255, 99, 132)',
                borderColor: 'rgb(255, 99, 132)',
                data: sentiMagnitudes,
            },
            {
                label: 'overall sentiment score',
                backgroundColor: 'rgb(000, 051, 204)',
                borderColor: 'rgb(000, 051, 204)',
                borderDash: [5, 5],
                data: overallScoreList,
            },
            {
                label: 'overall sentiment magnitude',
                backgroundColor: 'rgb(255, 000, 153)',
                borderColor: 'rgb(255, 000, 153)',
                borderDash: [5, 5],
                data: overallMagnitudeList,
            }
        ]
    };

    const config = {
        type: 'line',
        data: data,
        options: {
            responsive: true,
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: "The patient's sentiment analysis chart"
                }
            }
        },
    };

    const myChart = new Chart(
        document.getElementById('patientChart'),
        config
    );
}