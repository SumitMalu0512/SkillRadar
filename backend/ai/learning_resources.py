"""
Curated learning resource map for popular skills.
For each skill, we provide a small set of high-quality free/freemium resources.
"""

LEARNING_RESOURCES = {
    # Programming Languages
    "Python": [
        {"title": "Python.org Official Tutorial", "url": "https://docs.python.org/3/tutorial/", "type": "docs"},
        {"title": "freeCodeCamp Python Course", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "type": "course"},
        {"title": "CS50P (Harvard)", "url": "https://cs50.harvard.edu/python/", "type": "course"},
    ],
    "JavaScript": [
        {"title": "MDN JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "type": "docs"},
        {"title": "JavaScript.info", "url": "https://javascript.info/", "type": "tutorial"},
        {"title": "freeCodeCamp JS Algorithms", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "type": "course"},
    ],
    "TypeScript": [
        {"title": "TypeScript Handbook", "url": "https://www.typescriptlang.org/docs/handbook/intro.html", "type": "docs"},
        {"title": "Total TypeScript Beginners Tutorial", "url": "https://www.totaltypescript.com/tutorials/beginners-typescript", "type": "course"},
    ],
    "Java": [
        {"title": "Oracle Java Tutorials", "url": "https://docs.oracle.com/javase/tutorial/", "type": "docs"},
        {"title": "Java Programming - University of Helsinki", "url": "https://java-programming.mooc.fi/", "type": "course"},
    ],
    "C++": [
        {"title": "LearnCpp.com", "url": "https://www.learncpp.com/", "type": "tutorial"},
        {"title": "cppreference.com", "url": "https://en.cppreference.com/w/", "type": "docs"},
    ],
    "Go": [
        {"title": "A Tour of Go", "url": "https://go.dev/tour/", "type": "tutorial"},
        {"title": "Go by Example", "url": "https://gobyexample.com/", "type": "tutorial"},
    ],
    "Rust": [
        {"title": "The Rust Book", "url": "https://doc.rust-lang.org/book/", "type": "docs"},
        {"title": "Rustlings Exercises", "url": "https://github.com/rust-lang/rustlings", "type": "practice"},
    ],

    # Web Frontend
    "React": [
        {"title": "React Official Docs", "url": "https://react.dev/learn", "type": "docs"},
        {"title": "Scrimba React Course", "url": "https://scrimba.com/learn/learnreact", "type": "course"},
        {"title": "Epic React (Kent C. Dodds)", "url": "https://epicreact.dev/", "type": "course"},
    ],
    "Next.js": [
        {"title": "Next.js Learn", "url": "https://nextjs.org/learn", "type": "course"},
    ],
    "Vue.js": [
        {"title": "Vue.js Official Tutorial", "url": "https://vuejs.org/tutorial/", "type": "tutorial"},
    ],
    "Angular": [
        {"title": "Angular Tour of Heroes", "url": "https://angular.io/tutorial/tour-of-heroes", "type": "tutorial"},
    ],
    "HTML": [
        {"title": "MDN HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/HTML", "type": "docs"},
    ],
    "CSS": [
        {"title": "CSS Tricks Almanac", "url": "https://css-tricks.com/almanac/", "type": "docs"},
        {"title": "Flexbox Froggy (Game)", "url": "https://flexboxfroggy.com/", "type": "practice"},
    ],
    "Tailwind CSS": [
        {"title": "Tailwind Official Docs", "url": "https://tailwindcss.com/docs", "type": "docs"},
    ],

    # Backend
    "Node.js": [
        {"title": "Node.js Official Docs", "url": "https://nodejs.org/en/learn", "type": "docs"},
        {"title": "The Node.js Handbook", "url": "https://www.freecodecamp.org/news/the-definitive-node-js-handbook-6912378afc6e/", "type": "tutorial"},
    ],
    "Express.js": [
        {"title": "Express.js Docs", "url": "https://expressjs.com/", "type": "docs"},
    ],
    "Django": [
        {"title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "type": "tutorial"},
        {"title": "Django Girls Tutorial", "url": "https://tutorial.djangogirls.org/", "type": "tutorial"},
    ],
    "Flask": [
        {"title": "Flask Quickstart", "url": "https://flask.palletsprojects.com/en/latest/quickstart/", "type": "docs"},
        {"title": "Flask Mega Tutorial", "url": "https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world", "type": "tutorial"},
    ],
    "FastAPI": [
        {"title": "FastAPI Official Tutorial", "url": "https://fastapi.tiangolo.com/tutorial/", "type": "tutorial"},
    ],
    "Spring Boot": [
        {"title": "Spring Boot Getting Started", "url": "https://spring.io/guides/gs/spring-boot", "type": "tutorial"},
        {"title": "Baeldung Spring Boot", "url": "https://www.baeldung.com/spring-boot", "type": "tutorial"},
    ],

    # Databases
    "SQL": [
        {"title": "SQLBolt Interactive Tutorial", "url": "https://sqlbolt.com/", "type": "tutorial"},
        {"title": "Mode SQL Tutorial", "url": "https://mode.com/sql-tutorial/", "type": "tutorial"},
    ],
    "PostgreSQL": [
        {"title": "PostgreSQL Tutorial", "url": "https://www.postgresqltutorial.com/", "type": "tutorial"},
    ],
    "MongoDB": [
        {"title": "MongoDB University (Free)", "url": "https://university.mongodb.com/", "type": "course"},
    ],
    "MySQL": [
        {"title": "MySQL Tutorial", "url": "https://dev.mysql.com/doc/refman/8.0/en/tutorial.html", "type": "docs"},
    ],
    "Redis": [
        {"title": "Redis University", "url": "https://university.redis.com/", "type": "course"},
    ],

    # Cloud & DevOps
    "AWS": [
        {"title": "AWS Skill Builder (Free)", "url": "https://skillbuilder.aws/", "type": "course"},
        {"title": "AWS Cloud Practitioner Essentials", "url": "https://aws.amazon.com/training/digital/aws-cloud-practitioner-essentials/", "type": "course"},
    ],
    "Azure": [
        {"title": "Microsoft Learn - Azure", "url": "https://learn.microsoft.com/en-us/training/azure/", "type": "course"},
    ],
    "Google Cloud": [
        {"title": "Google Cloud Skills Boost", "url": "https://www.cloudskillsboost.google/", "type": "course"},
    ],
    "Docker": [
        {"title": "Docker Getting Started", "url": "https://docs.docker.com/get-started/", "type": "tutorial"},
        {"title": "Play with Docker", "url": "https://labs.play-with-docker.com/", "type": "practice"},
    ],
    "Kubernetes": [
        {"title": "Kubernetes Basics", "url": "https://kubernetes.io/docs/tutorials/kubernetes-basics/", "type": "tutorial"},
        {"title": "Killercoda K8s Playground", "url": "https://killercoda.com/playgrounds/scenario/kubernetes", "type": "practice"},
    ],
    "Terraform": [
        {"title": "HashiCorp Learn Terraform", "url": "https://developer.hashicorp.com/terraform/tutorials", "type": "tutorial"},
    ],
    "Jenkins": [
        {"title": "Jenkins Pipeline Tutorial", "url": "https://www.jenkins.io/doc/pipeline/tour/getting-started/", "type": "tutorial"},
    ],
    "CI/CD": [
        {"title": "GitHub Actions Quickstart", "url": "https://docs.github.com/en/actions/quickstart", "type": "tutorial"},
    ],
    "Linux": [
        {"title": "Linux Journey", "url": "https://linuxjourney.com/", "type": "tutorial"},
    ],

    # Data Science / ML / AI
    "Machine Learning": [
        {"title": "Andrew Ng's ML Course (Coursera)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "type": "course"},
        {"title": "Kaggle Learn ML", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "type": "course"},
    ],
    "Deep Learning": [
        {"title": "fast.ai Practical Deep Learning", "url": "https://course.fast.ai/", "type": "course"},
        {"title": "DeepLearning.AI Specialization", "url": "https://www.coursera.org/specializations/deep-learning", "type": "course"},
    ],
    "Natural Language Processing": [
        {"title": "Hugging Face NLP Course", "url": "https://huggingface.co/learn/nlp-course", "type": "course"},
        {"title": "Stanford CS224N Lectures", "url": "https://www.youtube.com/playlist?list=PLoROMvodv4rOSH4v6133s9LFPRHjEmbmJ", "type": "videos"},
    ],
    "Computer Vision": [
        {"title": "PyImageSearch Tutorials", "url": "https://pyimagesearch.com/start-here/", "type": "tutorial"},
    ],
    "TensorFlow": [
        {"title": "TensorFlow Tutorials", "url": "https://www.tensorflow.org/tutorials", "type": "tutorial"},
    ],
    "PyTorch": [
        {"title": "PyTorch Official Tutorials", "url": "https://pytorch.org/tutorials/", "type": "tutorial"},
    ],
    "Scikit-learn": [
        {"title": "Scikit-learn User Guide", "url": "https://scikit-learn.org/stable/user_guide.html", "type": "docs"},
    ],
    "Pandas": [
        {"title": "Kaggle Pandas Course", "url": "https://www.kaggle.com/learn/pandas", "type": "course"},
        {"title": "Pandas Official Docs", "url": "https://pandas.pydata.org/docs/getting_started/index.html", "type": "docs"},
    ],
    "NumPy": [
        {"title": "NumPy Absolute Beginner Guide", "url": "https://numpy.org/doc/stable/user/absolute_beginners.html", "type": "docs"},
    ],
    "Large Language Models": [
        {"title": "DeepLearning.AI Short Courses on LLMs", "url": "https://www.deeplearning.ai/short-courses/", "type": "course"},
        {"title": "LangChain Docs", "url": "https://python.langchain.com/docs/get_started/introduction", "type": "docs"},
    ],
    "Generative AI": [
        {"title": "Google Generative AI Learning Path", "url": "https://www.cloudskillsboost.google/paths/118", "type": "course"},
    ],

    # Big Data
    "Apache Spark": [
        {"title": "Databricks Spark Tutorials", "url": "https://www.databricks.com/spark/getting-started-with-apache-spark", "type": "tutorial"},
    ],
    "Apache Kafka": [
        {"title": "Confluent Kafka 101", "url": "https://developer.confluent.io/learn-kafka/", "type": "course"},
    ],
    "Apache Airflow": [
        {"title": "Airflow Tutorial", "url": "https://airflow.apache.org/docs/apache-airflow/stable/tutorial/index.html", "type": "tutorial"},
    ],

    # BI / Analytics
    "Power BI": [
        {"title": "Microsoft Learn Power BI", "url": "https://learn.microsoft.com/en-us/training/powerplatform/power-bi", "type": "course"},
    ],
    "Tableau": [
        {"title": "Tableau Free Training", "url": "https://www.tableau.com/learn/training/elearning", "type": "course"},
    ],
    "Excel": [
        {"title": "Microsoft Excel Training", "url": "https://support.microsoft.com/en-us/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb", "type": "course"},
    ],

    # Mobile
    "Android": [
        {"title": "Android Developer Codelabs", "url": "https://developer.android.com/courses", "type": "course"},
    ],
    "iOS": [
        {"title": "Apple Develop iOS Apps", "url": "https://developer.apple.com/tutorials/app-dev-training", "type": "tutorial"},
    ],
    "Flutter": [
        {"title": "Flutter Codelabs", "url": "https://docs.flutter.dev/codelabs", "type": "course"},
    ],
    "React Native": [
        {"title": "React Native Docs", "url": "https://reactnative.dev/docs/getting-started", "type": "docs"},
    ],

    # Tools
    "Git": [
        {"title": "Pro Git Book (Free)", "url": "https://git-scm.com/book/en/v2", "type": "docs"},
        {"title": "Learn Git Branching", "url": "https://learngitbranching.js.org/", "type": "practice"},
    ],
    "GitHub": [
        {"title": "GitHub Skills", "url": "https://skills.github.com/", "type": "course"},
    ],

    # Testing
    "Selenium": [
        {"title": "Selenium Official Docs", "url": "https://www.selenium.dev/documentation/", "type": "docs"},
    ],
    "Jest": [
        {"title": "Jest Getting Started", "url": "https://jestjs.io/docs/getting-started", "type": "docs"},
    ],

    # Architecture / Concepts
    "Microservices": [
        {"title": "Microservices.io Patterns", "url": "https://microservices.io/patterns/", "type": "docs"},
    ],
    "System Design": [
        {"title": "System Design Primer", "url": "https://github.com/donnemartin/system-design-primer", "type": "docs"},
        {"title": "ByteByteGo (YouTube)", "url": "https://www.youtube.com/@ByteByteGo", "type": "videos"},
    ],
    "Data Structures": [
        {"title": "NeetCode Roadmap", "url": "https://neetcode.io/roadmap", "type": "course"},
        {"title": "Visualgo - DSA Visualizations", "url": "https://visualgo.net/", "type": "practice"},
    ],
    "Algorithms": [
        {"title": "LeetCode Problems", "url": "https://leetcode.com/problemset/", "type": "practice"},
    ],
    "REST API": [
        {"title": "REST API Tutorial", "url": "https://restfulapi.net/", "type": "docs"},
    ],
    "GraphQL": [
        {"title": "How to GraphQL", "url": "https://www.howtographql.com/", "type": "tutorial"},
    ],

    # Security
    "Cybersecurity": [
        {"title": "TryHackMe", "url": "https://tryhackme.com/", "type": "practice"},
    ],
    "Penetration Testing": [
        {"title": "HackTheBox Academy", "url": "https://academy.hackthebox.com/", "type": "course"},
    ],

    # Methodology
    "Agile": [
        {"title": "Atlassian Agile Coach", "url": "https://www.atlassian.com/agile", "type": "docs"},
    ],
    "Scrum": [
        {"title": "Scrum Guide (Official)", "url": "https://scrumguides.org/scrum-guide.html", "type": "docs"},
    ],
}


def resources_for_skill(skill: str, limit: int = 3):
    """
    Get curated learning resources for a skill.
    If we don't have curated resources, generate a generic fallback search link.
    """
    if skill in LEARNING_RESOURCES:
        return LEARNING_RESOURCES[skill][:limit]

    # case-insensitive match fallback
    skill_lower = skill.lower()
    for canonical, resources in LEARNING_RESOURCES.items():
        if canonical.lower() == skill_lower:
            return resources[:limit]

    # generic fallback: search links
    return [
        {
            "title": f"Search YouTube for {skill}",
            "url": f"https://www.youtube.com/results?search_query={skill.replace(' ', '+')}+tutorial",
            "type": "videos",
        },
        {
            "title": f"freeCodeCamp articles on {skill}",
            "url": f"https://www.freecodecamp.org/news/search/?query={skill.replace(' ', '+')}",
            "type": "tutorial",
        },
        {
            "title": f"Find courses on Coursera",
            "url": f"https://www.coursera.org/search?query={skill.replace(' ', '+')}",
            "type": "course",
        },
    ][:limit]
