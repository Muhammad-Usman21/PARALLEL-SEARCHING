import pandas as pd
import random

def generate_random_student_info(num_students=10):
    """Generate random student information."""
    names = [
        "James", "William", "John", "Robert", "Michael", "Omar", "Yusuf", "Tariq", "Khalid", "Faisal",
        "Arjun", "Rohan", "Kunal", "Rajesh", "Vikram", "Wei", "Ming", "Jun", "Hao", "Lei",
        "Hiroshi", "Takumi", "Haruto", "Satoshi", "Kenta", "Kwame", "Tunde", "Jabari", "Thabo", "Ade",
        "Luca", "Sebastian", "Hugo", "Viktor", "Niels", "Lars", "Bjorn", "Erik", "Olav", "Aksel",
        "Diego", "Thiago", "Mateo", "Santiago", "Javier", "Min-jun", "Ji-ho", "Tae-hyun", "Dong-wook", "Hyun-soo",
        "David", "Benjamin", "Eli", "Ezra", "Aaron", "Emma", "Olivia", "Sophia", "Isabella", "Ava",
        "Aisha", "Fatima", "Layla", "Zainab", "Noor", "Priya", "Ananya", "Deepa", "Meera", "Sanya",
        "Li", "Xiao", "Mei", "Chun", "Ling", "Yumi", "Hana", "Sakura", "Rina", "Aiko",
        "Zola", "Ama", "Eshe", "Nia", "Imani", "Sophia", "Amelia", "Clara", "Elena", "Irene",
        "Freya", "Astrid", "Ingrid", "Sigrid", "Liv", "Camila", "Isabella", "Valeria", "Maria", "Luciana",
        "Ji-woo", "Seo-yeon", "Ha-eun", "Min-seo", "Su-bin", "Sarah", "Rachel", "Leah", "Miriam", "Hannah"
    ]
    countries = ["Pakistan", "India", "USA", "UK", "Australia", "Germany", "Canada", "China", "Japan", "South Africa"]
    cities = ["Lahore", "Karachi", "Islamabad", "Faisalabad", "Peshawar", "Multan", "Quetta", "Rawalpindi", "Sialkot", "Hyderabad", 
        "New York", "Los Angeles", "Chicago", "Houston", "Phoenix", "London", "Manchester", "Birmingham", "Leeds", "Glasgow", "Mumbai", 
        "Delhi", "Bangalore", "Chennai", "Hyderabad", "Beijing", "Shanghai", "Shenzhen", "Guangzhou", "Chengdu", "Tokyo", "Osaka", 
        "Kyoto", "Hiroshima", "Nagoya", "Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide", "Berlin", "Munich", "Hamburg", 
        "Frankfurt", "Cologne", "Johannesburg", "Cape Town", "Durban", "Pretoria", "Bloemfontein", "São Paulo", "Rio de Janeiro", 
        "Brasília", "Salvador", "Fortaleza"]

    courses = [
        "BSc CS", "BSc IT", "BBA", "BS Physics", "BS Mathematics", 
        "BS Chemistry", "BS Biology", "BS Biotechnology", "BS Microbiology", "BS Zoology", 
        "BS Botany", "BS Environmental Science", "BS Geology", "BS Geography", "BS Statistics",
        "BA English", "BA History", "BA Sociology", "BA Psychology", "BA Political Science",
        "BS Economics", "BS Finance", "BS Accounting", "BS Marketing", "BS Management",
        "BS Electrical Engineering", "BS Mechanical Engineering", "BS Civil Engineering", 
        "BS Software Engineering", "BS Aerospace Engineering", 
        "BS Data Science", "BS Artificial Intelligence", "BS Cybersecurity", "BS Robotics",
        "BS Nursing", "BS Medicine", "BS Pharmacy", "BS Medical Lab Technology", "BS Radiology",
        "BS Education", "BS Physical Education", "BS Social Work", "BS Journalism", 
        "BS Media Studies", "BS Film and TV", "BS Fine Arts", "BS Graphic Design",
        "BS Architecture", "BS Interior Design", "BS Fashion Design", "BS Textile Design",
        "LLB Law", "BS Criminology", "BS International Relations", 
        "BS Anthropology", "BS Linguistics", "BS Philosophy", "BS Islamic Studies", 
        "BS Religious Studies", "BS Tourism and Hospitality", 
        "BS Agriculture", "BS Food Science and Technology", 
        "BS Veterinary Science", "BS Forestry", "BS Fisheries", 
        "BS Oceanography", "BS Marine Biology", "BS Astronomy", 
        "BS Energy Science", "BS Renewable Energy"
    ]

    subjects = [
        "Mathematics", "Physics", "Chemistry", "Biology", "Statistics", 
        "Computer Science", "Data Science", "Artificial Intelligence", "Cybersecurity", "Software Engineering", 
        "Electrical Engineering", "Mechanical Engineering", "Civil Engineering", "Aerospace Engineering", "Robotics",
        "Economics", "Finance", "Accounting", "Marketing", "Management", 
        "History", "Geography", "Political Science", "Sociology", "Psychology", 
        "Philosophy", "Anthropology", "International Relations", "Linguistics", "Law",
        "English Literature", "Creative Writing", "Journalism", "Media Studies", "Film Studies",
        "Fine Arts", "Graphic Design", "Fashion Design", "Interior Design", "Textile Design", 
        "Environmental Science", "Geology", "Oceanography", "Marine Biology", "Astronomy", 
        "Medical Science", "Pharmacy", "Nursing", "Radiology", "Medical Lab Technology", 
        "Education", "Physical Education", "Social Work", "Religious Studies", "Islamic Studies", 
        "Tourism and Hospitality", "Food Science and Technology", "Agriculture", "Forestry", 
        "Fisheries", "Biotechnology", "Microbiology", "Zoology", "Botany",
        "Energy Science", "Renewable Energy", "Marine Science", "Veterinary Science", 
        "Business Administration", "Supply Chain Management", "Public Administration", 
        "Astronomy", "Astrophysics", "Nanotechnology", "Cryptography", "Game Development"
    ]    
   

    students = []
    for _ in range(num_students):
        num_subjects = random.randint(1, 6)  # Randomly choose number of subjects (1 to all subjects)
        
        student = {
            "Name": random.choice(names),
            "Roll Number": random.randint(1000, 9999),
            "Age": random.randint(18, 25),
            "City": random.choice(cities),
            "Country": random.choice(countries),
            "Course": random.choice(courses),
            "Subjects": ", ".join(random.sample(subjects, num_subjects)),
        }
        students.append(student)
    return students

def create_excel_files(num_files=5, min_students=5, max_students=15):
    """Create multiple Excel files with random student info."""
    for i in range(1, num_files + 1):
        # Randomize number of students for this file
        num_students = random.randint(min_students, max_students)
        
        # Generate random student info
        student_data = generate_random_student_info(num_students)
        
        # Create a DataFrame
        df = pd.DataFrame(student_data)
        
        # Create an Excel file
        filename = f"file{i}.xlsx"
        df.to_excel(filename, index=False)
        print(f"Generated file: {filename} with {num_students} students")

# Generate 3 Excel files with random number of students (between 5 and 15)
create_excel_files(num_files=10, min_students=400, max_students=900)