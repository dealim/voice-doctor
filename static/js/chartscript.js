// function initializeChart() {
//     let sentences = {{ patient.text_contents | tojson }};
//     let sentiScores = {{ patient.senti_scores | tojson }};
//     let sentiMagnitudes = {{ patient.senti_magnitudes | tojson }};
//     let overallScore = {{ patient.doc_sentiment_score | tojson }};
//     let overallMagnitude = {{ patient.doc_sentiment_magnitude | tojson }};
//
//     let overallScoreList = new Array(sentiScores.length).fill(overallScore);
//     let overallMagnitudeList = new Array(sentiScores.length).fill(overallMagnitude);
//
//     let labels = [];
//     for (let i = 1; i <= sentences.length; i++) {
//         labels.push("text" + i);
//     }
//
//     const data = {
//         labels: labels,
//         datasets: [
//             {
//                 label: 'sentiment scores',
//                 backgroundColor: 'rgb(000, 153, 255)',
//                 borderColor: 'rgb(000, 153, 255)',
//                 data: sentiScores,
//             },
//             {
//                 label: 'sentiment magnitudes',
//                 backgroundColor: 'rgb(255, 99, 132)',
//                 borderColor: 'rgb(255, 99, 132)',
//                 data: sentiMagnitudes,
//             },
//             {
//                 label: 'overall sentiment score',
//                 backgroundColor: 'rgb(000, 051, 204)',
//                 borderColor: 'rgb(000, 051, 204)',
//                 borderDash: [5, 5],
//                 data: overallScoreList,
//             },
//             {
//                 label: 'overall sentiment magnitude',
//                 backgroundColor: 'rgb(255, 000, 153)',
//                 borderColor: 'rgb(255, 000, 153)',
//                 borderDash: [5, 5],
//                 data: overallMagnitudeList,
//             }
//         ]
//     };
//
//     const config = {
//         type: 'line',
//         data: data,
//         options: {
//             responsive: true,
//             plugins: {
//                 legend: {
//                     position: 'top',
//                 },
//                 title: {
//                     display: true,
//                     text: "The patient's sentiment analysis chart"
//                 }
//             }
//         },
//     };
//
//     const myChart = new Chart(
//         document.getElementById('patientChart'),
//         config
//     );
// }