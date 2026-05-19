"""
Skill Taxonomy.

A curated dictionary of skills with aliases and categories.
We use this for keyword based skill extraction from job descriptions.

Categories help us cluster job roles and present analytics in a clean way.
Aliases let us normalize variations (e.g., "JS" -> "JavaScript", "ML" -> "Machine Learning").

This was built by combining O*NET skill data, Stack Overflow tags,
and Indian job market common skills.
"""

# Format: { canonical_name: { "category": str, "aliases": [list of variations] } }
# Aliases are matched case-insensitive

SKILL_TAXONOMY = {
    # ---------------- Programming Languages ----------------
    "Python": {"category": "Programming", "aliases": ["python3", "py"]},
    "JavaScript": {"category": "Programming", "aliases": ["js", "javascript", "ecmascript", "es6", "es2015"]},
    "TypeScript": {"category": "Programming", "aliases": ["ts", "typescript"]},
    "Java": {"category": "Programming", "aliases": ["java8", "java11", "core java"]},
    "C++": {"category": "Programming", "aliases": ["cpp", "c plus plus"]},
    "C#": {"category": "Programming", "aliases": ["csharp", "c-sharp", "dotnet c#"]},
    "C": {"category": "Programming", "aliases": ["c programming", "c language"]},
    "Go": {"category": "Programming", "aliases": ["golang", "go-lang"]},
    "Rust": {"category": "Programming", "aliases": ["rust-lang", "rustlang"]},
    "Ruby": {"category": "Programming", "aliases": ["ruby on rails dev"]},
    "PHP": {"category": "Programming", "aliases": ["php7", "php8"]},
    "Swift": {"category": "Programming", "aliases": ["swift programming"]},
    "Kotlin": {"category": "Programming", "aliases": ["kotlin lang"]},
    "Scala": {"category": "Programming", "aliases": []},
    "R": {"category": "Programming", "aliases": ["r programming", "r-lang"]},
    "MATLAB": {"category": "Programming", "aliases": ["matlab programming"]},
    "Perl": {"category": "Programming", "aliases": []},
    "Dart": {"category": "Programming", "aliases": ["dart lang"]},
    "Objective-C": {"category": "Programming", "aliases": ["objective c", "objc"]},
    "Shell Scripting": {"category": "Programming", "aliases": ["bash", "shell", "shell script", "bash scripting"]},
    "PowerShell": {"category": "Programming", "aliases": ["ps1", "windows powershell"]},
    "Assembly": {"category": "Programming", "aliases": ["assembly language", "asm"]},
    "Solidity": {"category": "Programming", "aliases": ["solidity lang"]},

    # ---------------- Web Frontend ----------------
    "HTML": {"category": "Web Frontend", "aliases": ["html5", "html 5"]},
    "CSS": {"category": "Web Frontend", "aliases": ["css3", "css 3"]},
    "React": {"category": "Web Frontend", "aliases": ["react.js", "reactjs", "react js"]},
    "Vue.js": {"category": "Web Frontend", "aliases": ["vue", "vuejs", "vue js", "vue 3"]},
    "Angular": {"category": "Web Frontend", "aliases": ["angularjs", "angular.js", "angular 2+"]},
    "Next.js": {"category": "Web Frontend", "aliases": ["nextjs", "next js"]},
    "Nuxt.js": {"category": "Web Frontend", "aliases": ["nuxtjs", "nuxt"]},
    "Svelte": {"category": "Web Frontend", "aliases": ["sveltejs", "svelte kit", "sveltekit"]},
    "jQuery": {"category": "Web Frontend", "aliases": ["jquery js"]},
    "Bootstrap": {"category": "Web Frontend", "aliases": ["bootstrap 5", "bootstrap4"]},
    "Tailwind CSS": {"category": "Web Frontend", "aliases": ["tailwind", "tailwindcss"]},
    "Material UI": {"category": "Web Frontend", "aliases": ["mui", "material-ui"]},
    "Sass": {"category": "Web Frontend", "aliases": ["scss", "sass css"]},
    "Webpack": {"category": "Web Frontend", "aliases": ["web pack"]},
    "Vite": {"category": "Web Frontend", "aliases": ["vitejs"]},
    "Redux": {"category": "Web Frontend", "aliases": ["redux toolkit", "rtk"]},

    # ---------------- Web Backend / Frameworks ----------------
    "Node.js": {"category": "Web Backend", "aliases": ["nodejs", "node js", "node"]},
    "Express.js": {"category": "Web Backend", "aliases": ["express", "expressjs"]},
    "Django": {"category": "Web Backend", "aliases": ["django framework", "django rest"]},
    "Flask": {"category": "Web Backend", "aliases": ["flask framework"]},
    "FastAPI": {"category": "Web Backend", "aliases": ["fast api"]},
    "Spring Boot": {"category": "Web Backend", "aliases": ["springboot", "spring-boot", "spring"]},
    "Ruby on Rails": {"category": "Web Backend", "aliases": ["rails", "ror"]},
    "Laravel": {"category": "Web Backend", "aliases": ["laravel framework"]},
    "ASP.NET": {"category": "Web Backend", "aliases": ["asp .net", "aspnet", ".net core", "dotnet core", ".net"]},
    "NestJS": {"category": "Web Backend", "aliases": ["nest.js", "nestjs framework"]},
    "GraphQL": {"category": "Web Backend", "aliases": ["graph ql", "apollo graphql"]},
    "REST API": {"category": "Web Backend", "aliases": ["restful api", "rest", "rest apis", "restful"]},
    "gRPC": {"category": "Web Backend", "aliases": ["grpc protocol"]},
    "WebSocket": {"category": "Web Backend", "aliases": ["websockets", "socket.io", "socketio"]},

    # ---------------- Databases ----------------
    "SQL": {"category": "Database", "aliases": ["structured query language"]},
    "MySQL": {"category": "Database", "aliases": ["my sql"]},
    "PostgreSQL": {"category": "Database", "aliases": ["postgres", "postgre sql", "psql"]},
    "MongoDB": {"category": "Database", "aliases": ["mongo db", "mongo"]},
    "Redis": {"category": "Database", "aliases": []},
    "Elasticsearch": {"category": "Database", "aliases": ["elastic search", "elk stack"]},
    "Cassandra": {"category": "Database", "aliases": ["apache cassandra"]},
    "Oracle": {"category": "Database", "aliases": ["oracle db", "oracle database"]},
    "SQL Server": {"category": "Database", "aliases": ["mssql", "ms sql", "microsoft sql"]},
    "SQLite": {"category": "Database", "aliases": ["sqlite3"]},
    "DynamoDB": {"category": "Database", "aliases": ["dynamo db", "amazon dynamodb"]},
    "Firebase": {"category": "Database", "aliases": ["firebase firestore", "firestore", "google firebase"]},
    "Supabase": {"category": "Database", "aliases": []},
    "Neo4j": {"category": "Database", "aliases": ["neo 4j", "graph database"]},
    "MariaDB": {"category": "Database", "aliases": ["maria db"]},
    "Snowflake": {"category": "Database", "aliases": ["snowflake db"]},
    "BigQuery": {"category": "Database", "aliases": ["google bigquery", "big query"]},

    # ---------------- Cloud & DevOps ----------------
    "AWS": {"category": "Cloud", "aliases": ["amazon web services", "amazon aws"]},
    "Azure": {"category": "Cloud", "aliases": ["microsoft azure", "ms azure"]},
    "Google Cloud": {"category": "Cloud", "aliases": ["gcp", "google cloud platform"]},
    "Heroku": {"category": "Cloud", "aliases": []},
    "DigitalOcean": {"category": "Cloud", "aliases": ["digital ocean"]},
    "Vercel": {"category": "Cloud", "aliases": []},
    "Netlify": {"category": "Cloud", "aliases": []},
    "Docker": {"category": "DevOps", "aliases": ["dockerize", "docker container"]},
    "Kubernetes": {"category": "DevOps", "aliases": ["k8s", "kube"]},
    "Jenkins": {"category": "DevOps", "aliases": ["jenkins ci"]},
    "GitHub Actions": {"category": "DevOps", "aliases": ["github action", "gh actions"]},
    "GitLab CI": {"category": "DevOps", "aliases": ["gitlab cicd", "gitlab pipelines"]},
    "CircleCI": {"category": "DevOps", "aliases": ["circle ci"]},
    "Terraform": {"category": "DevOps", "aliases": ["terraform iac"]},
    "Ansible": {"category": "DevOps", "aliases": ["ansible automation"]},
    "Puppet": {"category": "DevOps", "aliases": []},
    "Chef": {"category": "DevOps", "aliases": ["chef config"]},
    "Nginx": {"category": "DevOps", "aliases": []},
    "Apache": {"category": "DevOps", "aliases": ["apache http", "httpd"]},
    "Linux": {"category": "DevOps", "aliases": ["linux admin", "linux administration", "unix"]},
    "CI/CD": {"category": "DevOps", "aliases": ["cicd", "ci cd", "continuous integration"]},
    "Prometheus": {"category": "DevOps", "aliases": []},
    "Grafana": {"category": "DevOps", "aliases": []},
    "Datadog": {"category": "DevOps", "aliases": ["data dog"]},

    # ---------------- Data Science / ML / AI ----------------
    "Machine Learning": {"category": "Data Science", "aliases": ["ml", "machine-learning"]},
    "Deep Learning": {"category": "Data Science", "aliases": ["dl", "deep-learning"]},
    "Natural Language Processing": {"category": "Data Science", "aliases": ["nlp", "natural-language-processing"]},
    "Computer Vision": {"category": "Data Science", "aliases": ["cv", "computer-vision", "image processing"]},
    "Reinforcement Learning": {"category": "Data Science", "aliases": ["rl", "reinforcement-learning"]},
    "Generative AI": {"category": "Data Science", "aliases": ["genai", "generative ai", "gen ai"]},
    "Large Language Models": {"category": "Data Science", "aliases": ["llm", "llms", "large language model"]},
    "TensorFlow": {"category": "Data Science", "aliases": ["tensor flow", "tf"]},
    "PyTorch": {"category": "Data Science", "aliases": ["py torch", "torch"]},
    "Keras": {"category": "Data Science", "aliases": []},
    "Scikit-learn": {"category": "Data Science", "aliases": ["sklearn", "scikit learn"]},
    "Pandas": {"category": "Data Science", "aliases": ["pandas library"]},
    "NumPy": {"category": "Data Science", "aliases": ["numpy library", "num py"]},
    "Matplotlib": {"category": "Data Science", "aliases": ["matplot lib"]},
    "Seaborn": {"category": "Data Science", "aliases": []},
    "Plotly": {"category": "Data Science", "aliases": []},
    "spaCy": {"category": "Data Science", "aliases": ["spacy nlp", "spacy"]},
    "NLTK": {"category": "Data Science", "aliases": ["natural language toolkit"]},
    "Hugging Face": {"category": "Data Science", "aliases": ["huggingface", "transformers library"]},
    "OpenCV": {"category": "Data Science", "aliases": ["open cv", "cv2"]},
    "XGBoost": {"category": "Data Science", "aliases": ["xg boost"]},
    "LightGBM": {"category": "Data Science", "aliases": ["light gbm", "lgbm"]},
    "Statistical Modeling": {"category": "Data Science", "aliases": ["statistics", "statistical analysis"]},
    "Time Series Analysis": {"category": "Data Science", "aliases": ["timeseries", "time-series"]},
    "Predictive Modeling": {"category": "Data Science", "aliases": ["predictive analytics"]},
    "Feature Engineering": {"category": "Data Science", "aliases": []},
    "Data Mining": {"category": "Data Science", "aliases": ["data-mining"]},
    "Data Visualization": {"category": "Data Science", "aliases": ["data viz", "dataviz"]},
    "A/B Testing": {"category": "Data Science", "aliases": ["ab testing", "a b testing", "split testing"]},

    # ---------------- Data Engineering / Big Data ----------------
    "Apache Spark": {"category": "Big Data", "aliases": ["spark", "pyspark"]},
    "Apache Kafka": {"category": "Big Data", "aliases": ["kafka", "kafka streams"]},
    "Hadoop": {"category": "Big Data", "aliases": ["apache hadoop", "hdfs"]},
    "Apache Airflow": {"category": "Big Data", "aliases": ["airflow"]},
    "Databricks": {"category": "Big Data", "aliases": ["data bricks"]},
    "ETL": {"category": "Big Data", "aliases": ["extract transform load", "etl pipeline"]},
    "Data Pipeline": {"category": "Big Data", "aliases": ["data pipelines"]},
    "Apache Flink": {"category": "Big Data", "aliases": ["flink"]},
    "Apache Beam": {"category": "Big Data", "aliases": ["beam"]},
    "dbt": {"category": "Big Data", "aliases": ["data build tool"]},

    # ---------------- BI / Analytics Tools ----------------
    "Power BI": {"category": "Analytics", "aliases": ["powerbi", "power-bi", "ms power bi"]},
    "Tableau": {"category": "Analytics", "aliases": ["tableau desktop"]},
    "Looker": {"category": "Analytics", "aliases": ["google looker"]},
    "Excel": {"category": "Analytics", "aliases": ["microsoft excel", "ms excel", "advanced excel"]},
    "Google Sheets": {"category": "Analytics", "aliases": ["g sheets", "gsheets"]},
    "Qlik": {"category": "Analytics", "aliases": ["qlikview", "qlik sense"]},
    "Metabase": {"category": "Analytics", "aliases": []},

    # ---------------- Mobile Development ----------------
    "Android": {"category": "Mobile", "aliases": ["android development", "android dev"]},
    "iOS": {"category": "Mobile", "aliases": ["ios development", "apple ios"]},
    "React Native": {"category": "Mobile", "aliases": ["react-native", "reactnative"]},
    "Flutter": {"category": "Mobile", "aliases": ["flutter dev"]},
    "Xamarin": {"category": "Mobile", "aliases": []},
    "Ionic": {"category": "Mobile", "aliases": ["ionic framework"]},
    "SwiftUI": {"category": "Mobile", "aliases": ["swift ui"]},
    "Jetpack Compose": {"category": "Mobile", "aliases": ["compose android"]},

    # ---------------- Version Control & Collaboration ----------------
    "Git": {"category": "Tools", "aliases": ["git scm"]},
    "GitHub": {"category": "Tools", "aliases": ["git hub"]},
    "GitLab": {"category": "Tools", "aliases": ["git lab"]},
    "Bitbucket": {"category": "Tools", "aliases": ["bit bucket"]},
    "Jira": {"category": "Tools", "aliases": ["atlassian jira"]},
    "Confluence": {"category": "Tools", "aliases": ["atlassian confluence"]},
    "Slack": {"category": "Tools", "aliases": []},
    "Notion": {"category": "Tools", "aliases": []},
    "Figma": {"category": "Tools", "aliases": []},
    "Postman": {"category": "Tools", "aliases": []},

    # ---------------- Security / Networking ----------------
    "Cybersecurity": {"category": "Security", "aliases": ["cyber security", "info sec", "infosec"]},
    "Penetration Testing": {"category": "Security", "aliases": ["pen testing", "pentest", "pentesting"]},
    "Ethical Hacking": {"category": "Security", "aliases": ["ethical hacker"]},
    "Network Security": {"category": "Security", "aliases": ["network sec"]},
    "OWASP": {"category": "Security", "aliases": []},
    "SSL/TLS": {"category": "Security", "aliases": ["ssl", "tls"]},
    "OAuth": {"category": "Security", "aliases": ["oauth2", "oauth 2.0"]},
    "JWT": {"category": "Security", "aliases": ["json web token", "json-web-token"]},
    "Cryptography": {"category": "Security", "aliases": ["cryptographic"]},
    "Firewall": {"category": "Security", "aliases": []},
    "VPN": {"category": "Security", "aliases": ["virtual private network"]},
    "TCP/IP": {"category": "Networking", "aliases": ["tcp ip", "tcpip"]},
    "DNS": {"category": "Networking", "aliases": ["domain name system"]},

    # ---------------- Testing / QA ----------------
    "Selenium": {"category": "Testing", "aliases": ["selenium webdriver"]},
    "Cypress": {"category": "Testing", "aliases": ["cypress io"]},
    "Jest": {"category": "Testing", "aliases": ["jest testing"]},
    "Mocha": {"category": "Testing", "aliases": ["mocha js"]},
    "JUnit": {"category": "Testing", "aliases": ["j unit", "junit 5"]},
    "PyTest": {"category": "Testing", "aliases": ["py test", "pytest"]},
    "Playwright": {"category": "Testing", "aliases": []},
    "Appium": {"category": "Testing", "aliases": []},
    "JMeter": {"category": "Testing", "aliases": ["j meter", "apache jmeter"]},
    "Manual Testing": {"category": "Testing", "aliases": ["manual qa"]},
    "Automation Testing": {"category": "Testing", "aliases": ["test automation", "automated testing"]},
    "Unit Testing": {"category": "Testing", "aliases": []},
    "Integration Testing": {"category": "Testing", "aliases": []},
    "TDD": {"category": "Testing", "aliases": ["test driven development", "test-driven development"]},

    # ---------------- Software Architecture & Concepts ----------------
    "Microservices": {"category": "Architecture", "aliases": ["micro services", "microservice"]},
    "Object-Oriented Programming": {"category": "Architecture", "aliases": ["oop", "object oriented"]},
    "Functional Programming": {"category": "Architecture", "aliases": ["fp"]},
    "Design Patterns": {"category": "Architecture", "aliases": ["design pattern"]},
    "System Design": {"category": "Architecture", "aliases": ["systems design"]},
    "Data Structures": {"category": "Architecture", "aliases": ["dsa", "data structure"]},
    "Algorithms": {"category": "Architecture", "aliases": ["algorithm design", "algo"]},
    "Distributed Systems": {"category": "Architecture", "aliases": ["distributed computing"]},
    "Event-Driven Architecture": {"category": "Architecture", "aliases": ["event driven", "eda"]},
    "Domain-Driven Design": {"category": "Architecture", "aliases": ["ddd", "domain driven"]},
    "MVC": {"category": "Architecture", "aliases": ["model view controller"]},
    "Serverless": {"category": "Architecture", "aliases": ["serverless architecture"]},

    # ---------------- Methodologies ----------------
    "Agile": {"category": "Methodology", "aliases": ["agile methodology", "agile development"]},
    "Scrum": {"category": "Methodology", "aliases": ["scrum master"]},
    "Kanban": {"category": "Methodology", "aliases": []},
    "Waterfall": {"category": "Methodology", "aliases": ["waterfall model"]},
    "DevOps": {"category": "Methodology", "aliases": ["dev ops", "devops practices"]},
    "SAFe": {"category": "Methodology", "aliases": ["scaled agile"]},

    # ---------------- Soft Skills (common asks) ----------------
    "Communication": {"category": "Soft Skills", "aliases": ["communication skills", "verbal communication"]},
    "Leadership": {"category": "Soft Skills", "aliases": ["team leadership", "leadership skills"]},
    "Problem Solving": {"category": "Soft Skills", "aliases": ["problem-solving", "analytical thinking"]},
    "Teamwork": {"category": "Soft Skills", "aliases": ["team work", "team player", "collaboration"]},
    "Critical Thinking": {"category": "Soft Skills", "aliases": ["critical-thinking"]},
    "Time Management": {"category": "Soft Skills", "aliases": []},
    "Project Management": {"category": "Soft Skills", "aliases": ["pm", "project mgmt"]},
    "Stakeholder Management": {"category": "Soft Skills", "aliases": ["stakeholder mgmt"]},
    "Presentation Skills": {"category": "Soft Skills", "aliases": ["presentation"]},
    "Adaptability": {"category": "Soft Skills", "aliases": ["adaptive"]},
    "Mentoring": {"category": "Soft Skills", "aliases": ["mentorship", "coaching"]},
}


def build_lookup_index():
    """
    Build a fast lookup dictionary: alias_lowercase -> canonical_name.
    This is what the extractor uses for matching.
    """
    lookup = {}
    for canonical, info in SKILL_TAXONOMY.items():
        # the canonical name itself is a "match"
        lookup[canonical.lower()] = canonical
        # add all aliases
        for alias in info.get("aliases", []):
            lookup[alias.lower()] = canonical
    return lookup


def get_category(skill_name: str) -> str:
    """Return the category for a canonical skill name. Defaults to 'Other'."""
    return SKILL_TAXONOMY.get(skill_name, {}).get("category", "Other")


def all_categories():
    """List of unique categories in the taxonomy."""
    return sorted(set(info["category"] for info in SKILL_TAXONOMY.values()))


def skills_in_category(category: str):
    """All canonical skill names in a given category."""
    return [
        name for name, info in SKILL_TAXONOMY.items()
        if info["category"] == category
    ]


# total stats - for sanity check
if __name__ == "__main__":
    print(f"Total skills in taxonomy: {len(SKILL_TAXONOMY)}")
    print(f"Categories: {all_categories()}")
    total_aliases = sum(len(info["aliases"]) for info in SKILL_TAXONOMY.values())
    print(f"Total aliases: {total_aliases}")
    print(f"Lookup index size: {len(build_lookup_index())}")
