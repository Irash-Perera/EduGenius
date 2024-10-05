import streamlit as st

st.html("""
        <!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>EduGenius - AI-Powered Math Tutoring</title>
    <style>
      @import url('https://fonts.googleapis.com/css2?family=Poppins:ital,wght@0,100;0,200;0,300;0,400;0,500;0,600;0,700;0,800;0,900;1,100;1,200;1,300;1,400;1,500;1,600;1,700;1,800;1,900&display=swap');

        :root {
            --primary-color: rgb(0,0,0,0);
            --secondary-color: #FFD700;
            --background-color: #FFF5E6;
            --text-color: rgb(0,0,0);
            --accent-color: rgb(255,255,255,0.2);
        }

        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: var(--text-color);
            background-color: var(--background-color);
            margin: 0;
            padding: 0;
        }

        .edu-header {
            background-color: var(--primary-color);
            color: white;
            padding: 4rem 0;
            position: relative;
            overflow: hidden;
            height: 300px;
        }

        .edu-header-content {
            position: relative;
            z-index: 2;
            text-align: center;
        }

        .edu-animated-bg {
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            overflow: hidden;
        }

        .edu-math-symbol {
            position: absolute;
            font-size: 2rem;
            opacity: 0.2;
            color: var(--secondary-color);
        }

        @keyframes float1 {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            25% { transform: translate(10px, -10px) rotate(5deg); }
            50% { transform: translate(20px, 0) rotate(10deg); }
            75% { transform: translate(10px, 10px) rotate(5deg); }
        }

        @keyframes float2 {
            0%, 100% { transform: translate(0, 0) rotate(0deg); }
            33% { transform: translate(-15px, 15px) rotate(-8deg); }
            66% { transform: translate(15px, -15px) rotate(8deg); }
        }

        @keyframes float3 {
            0%, 100% { transform: translate(0, 0) scale(1); }
            50% { transform: translate(5px, -5px) scale(1.1); }
        }

        @keyframes float4 {
            0%, 100% { transform: translateY(0) rotate(0deg); }
            50% { transform: translateY(-20px) rotate(180deg); }
        }

        .edu-math-symbol:nth-child(4n+1) {
            animation: float1 6s infinite;
        }

        .edu-math-symbol:nth-child(4n+2) {
            animation: float2 8s infinite;
        }

        .edu-math-symbol:nth-child(4n+3) {
            animation: float3 7s infinite;
        }

        .edu-math-symbol:nth-child(4n) {
            animation: float4 10s infinite;
        }

        .edu-title {
            font-family: 'Poppins', sans-serif;
            font-size: 6rem;
            margin: 0;
            font-weight: 500;
        }

        .edu-tagline {
            font-size: 1.4rem;
            margin-top: 1rem;
            opacity: 0.9;
        }

        .edu-container {
            max-width: 900px;
            margin: 0 auto;
            padding: 2rem;
        }

        .edu-content {
            border: 2px solid var(--accent-color);
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            padding: 2rem;
            margin-top: 2rem;
            animation: fadeIn 0.5s ease-out forwards;
            opacity: 0;
        }

        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }

        .edu-content:nth-child(1) { animation-delay: 0.2s; }
        .edu-content:nth-child(2) { animation-delay: 0.4s; }
        .edu-content:nth-child(3) { animation-delay: 0.6s; }

        .edu-subheader {
            font-size: 1.8rem;
            border-bottom: 2px solid var(--accent-color);
            padding-bottom: 0.5rem;
            margin-top: 0;
            color: rgb(255, 255, 255);
        }

        .edu-list {
            padding-left: 1.5rem;
            list-style-type: none;
        }

        .edu-list-item {
            margin-bottom: 1rem;
            position: relative;
            padding-left: 1.5rem;
        }

        .edu-list-item::before {
            content: '🚀';
            position: absolute;
            left: 0;
            top: 0;
        }

        .edu-highlight {
            color: rgb(255, 255, 255);
            font-weight: bold;
        }


        @media (max-width: 600px) {
            .edu-container {
                padding: 1rem;
            }

            .edu-title {
                font-size: 3rem;
            }

            .edu-subheader {
                font-size: 1.5rem;
            }
        }
    </style>
</head>
<body>
    <header class="edu-header">
        <div class="edu-header-content">
            <h1 class="edu-title">EduGenius</h1>
            <p class="edu-tagline">Learn Smarter. Get Personalized Help.</p>
        </div>
        <div class="edu-animated-bg">
            <div class="edu-math-symbol" style="top: 10%; left: 5%;">∑</div>
            <div class="edu-math-symbol" style="top: 30%; left: 15%;">∫</div>
            <div class="edu-math-symbol" style="top: 50%; left: 25%;">∏</div>
            <div class="edu-math-symbol" style="top: 70%; left: 35%;">√</div>
            <div class="edu-math-symbol" style="top: 20%; left: 45%;">∞</div>
            <div class="edu-math-symbol" style="top: 40%; left: 55%;">π</div>
            <div class="edu-math-symbol" style="top: 60%; left: 65%;">θ</div>
            <div class="edu-math-symbol" style="top: 80%; left: 75%;">Δ</div>
            <div class="edu-math-symbol" style="top: 15%; left: 85%;">λ</div>
            <div class="edu-math-symbol" style="top: 35%; left: 95%;">∂</div>
            <div class="edu-math-symbol" style="top: 55%; left: 5%;">∇</div>
            <div class="edu-math-symbol" style="top: 75%; left: 15%;">∈</div>
            <div class="edu-math-symbol" style="top: 25%; left: 25%;">∉</div>
            <div class="edu-math-symbol" style="top: 45%; left: 35%;">∪</div>
            <div class="edu-math-symbol" style="top: 65%; left: 45%;">∩</div>
            <div class="edu-math-symbol" style="top: 85%; left: 55%;">≈</div>
            <div class="edu-math-symbol" style="top: 5%; left: 65%;">≠</div>
            <div class="edu-math-symbol" style="top: 25%; left: 75%;">≤</div>
            <div class="edu-math-symbol" style="top: 45%; left: 85%;">≥</div>
            <div class="edu-math-symbol" style="top: 65%; left: 95%;">±</div>
        </div>
    </header>

    <div class="edu-container">
        <div class="edu-content">
            <h2 class="edu-subheader">What is EduGenius❓</h2>
            <p>In modern education, personalized and efficient tutoring remains a challenge, particularly in mathematics. Traditional tutoring methods often lack flexibility and efficiency, hindering the learning process. EduGenius steps in to revolutionize math education with cutting-edge AI technology.</p>
        </div>

        <div class="edu-content">
            <h2 class="edu-subheader">Our Mission 🎯</h2>
            <p>EduGenius aims to provide a personalized and efficient AI-powered tutoring system for A/Level and O/Level students in mathematics. We're committed to making advanced math education accessible, engaging, and tailored to each student's unique learning journey.</p>
        </div>

        <div class="edu-content">
            <h2 class="edu-subheader">Key Features 🚀</h2>
            <ul class="edu-list">
                <li class="edu-list-item"><span class="edu-highlight">Personalized Tutoring Materials:</span> Utilizes pre-processed and pre-stored maths marking schemes in our advanced vector database.</li>
                <li class="edu-list-item"><span class="edu-highlight">Cutting-Edge Technologies:</span> Leverages the latest in AI with LangChain, computational power with Wolfram, and state-of-the-art language models like Gemini.</li>
                <li class="edu-list-item"><span class="edu-highlight">Interactive Learning:</span> Generates dynamic and personalized tutoring materials that adapt to each student's progress.</li>
                <li class="edu-list-item"><span class="edu-highlight">Real-Time Evaluation:</span> Continuously assesses student performance, providing instant insights into areas of strength and improvement.</li>
                <li class="edu-list-item"><span class="edu-highlight">Instant Feedback:</span> Delivers immediate, accurate feedback and grades, accelerating the learning process.</li>
                <li class="edu-list-item"><span class="edu-highlight">Enhanced Learning Experience:</span> Creates an engaging, supportive environment that motivates students to excel in their mathematical journey.</li>
            </ul>

            <p>Ready to transform your math learning experience? Dive into the world of EduGenius today!</p>
        </div>
    </div>
</body>
</html>
        """)
 