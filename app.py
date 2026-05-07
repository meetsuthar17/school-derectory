import streamlit as st
import requests

BASE_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="School System", layout="wide")

# ---------------- PROFESSIONAL CSS ----------------
st.markdown("""
<style>

html, body, [class*="css"] {
    background: linear-gradient(135deg, #0f172a, #1e293b);
    color: white;
    font-family: 'Segoe UI', sans-serif;
}

section[data-testid="stSidebar"] {
    background: #020617;
    border-right: 1px solid #334155;
}

.title {
    font-size: 32px;
    font-weight: 700;
    margin-bottom: 15px;
}

.card {
    padding: 25px;
    border-radius: 18px;
    background: rgba(255,255,255,0.05);
    backdrop-filter: blur(12px);
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 25px rgba(0,0,0,0.4);
    margin-bottom: 15px;
}

.metric {
    font-size: 40px;
    font-weight: bold;
}

.stButton>button {
    width: 100%;
    border-radius: 12px;
    height: 45px;
    background: linear-gradient(135deg, #3b82f6, #6366f1);
    color: white;
    border: none;
    font-weight: 600;
}

</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<h2 style='text-align:center;'>🎓 School Management System</h2>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("🎓 School System")

menu = st.sidebar.radio(
    "Navigation",
    [
        "Dashboard",
        "Students",
        "Search Students",
        "Add Students",
        "Update Details",
        "Delete Students",
        "Teachers",
        "Subjects"
    ]
)

# ---------------- HELPER ----------------
def fetch(url):
    try:
        return requests.get(url).json()
    except:
        st.error("🚨 Backend not running")
        st.stop()

# ---------------- DASHBOARD ----------------
if menu == "Dashboard":

    st.markdown('<p class="title">📊 Dashboard</p>', unsafe_allow_html=True)

    students = fetch(f"{BASE_URL}/students")
    teachers = fetch(f"{BASE_URL}/teachers")
    departments = fetch(f"{BASE_URL}/departments")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
        <div class="card">
            <div class="metric">{len(students)}</div>
            👨‍🎓 Students
        </div>
        """, unsafe_allow_html=True)

    with col2:
        st.markdown(f"""
        <div class="card">
            <div class="metric">{len(teachers)}</div>
            👨‍🏫 Teachers
        </div>
        """, unsafe_allow_html=True)

    with col3:
        st.markdown(f"""
        <div class="card">
            <div class="metric">{len(departments)}</div>
            🏫 Departments
        </div>
        """, unsafe_allow_html=True)

# ---------------- STUDENTS ----------------
elif menu == "Students":

    st.markdown('<p class="title">👨‍🎓 Students</p>', unsafe_allow_html=True)

    data = fetch(f"{BASE_URL}/students")

    search = st.text_input("🔍 Search by Name")

    if search:
        data = [s for s in data if search.lower() in s["sname"].lower()]

    st.dataframe(data, use_container_width=True)

# ---------------- SEARCH STUDENTS ----------------
elif menu == "Search Students":

    st.markdown('<p class="title">🔍 Search Student</p>', unsafe_allow_html=True)

    search_type = st.radio("Search By", ["Student ID", "Department ID"])

    # -------- SEARCH BY SID --------
    if search_type == "Student ID":

        sid = st.number_input("Enter Student ID", min_value=1)

        if st.button("Search Student", key="sid_btn"):

            res = requests.get(f"{BASE_URL}/students/{sid}")

            if res.status_code == 200:
                data = res.json()

                st.markdown(f"""
                <div class="card">
                    <h4>👨‍🎓 {data['sname']}</h4>
                    <p><b>ID:</b> {data['sid']}</p>
                    <p><b>Roll No:</b> {data['rollno']}</p>
                    <p><b>Department:</b> {data['department_id']}</p>
                </div>
                """, unsafe_allow_html=True)

            else:
                st.error(res.json())

    # -------- SEARCH BY DID --------
    else:

        did = st.number_input("Enter Department ID", min_value=1)

        if st.button("Search Department Students", key="did_btn"):

            res = requests.get(f"{BASE_URL}/students/department/{did}")

            if res.status_code == 200:
                data = res.json()

                st.success(f"Found {len(data)} students")

                for s in data:
                    st.markdown(f"""
                    <div class="card">
                        <h4>👨‍🎓 {s['sname']}</h4>
                        <p><b>ID:</b> {s['sid']}</p>
                        <p><b>Roll No:</b> {s['rollno']}</p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.error(res.json())

# ---------------- ADD ----------------
elif menu == "Add Students":

    st.markdown('<p class="title">➕ Add Student</p>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    sid = col1.number_input("Student ID", min_value=1)
    name = col2.text_input("Name")

    roll = col1.number_input("Roll No", min_value=1)
    did = col2.number_input("Department ID", min_value=1)

    if st.button("Add Student"):

        res = requests.post(
            f"{BASE_URL}/students",
            data={
                "sid": sid,
                "sname": name,
                "rollno": roll,
                "did": did
            }
        )

        if res.status_code == 200:
            st.success("✅ Added Successfully")
        else:
            st.error(res.json())

# ---------------- UPDATE ----------------
elif menu == "Update Details":

    st.markdown('<p class="title">✏️ Update Student</p>', unsafe_allow_html=True)

    sid = st.number_input("Student ID", min_value=1)

    col1, col2 = st.columns(2)

    name = col1.text_input("New Name")
    roll = col2.number_input("New Roll No", min_value=1)
    did = col1.number_input("New Department ID", min_value=1)

    if st.button("Update"):

        res = requests.put(
            f"{BASE_URL}/students/{sid}",
            data={
                "sname": name,
                "rollno": roll,
                "did": did
            }
        )

        if res.status_code == 200:
            st.success("✅ Updated")
        else:
            st.error(res.json())

# ---------------- DELETE ----------------
elif menu == "Delete Students":

    st.markdown('<p class="title">❌ Delete Student</p>', unsafe_allow_html=True)

    sid = st.number_input("Student ID", min_value=1)

    if st.button("Delete"):

        res = requests.delete(f"{BASE_URL}/students/{sid}")

        if res.status_code == 200:
            st.success("Deleted Successfully")
        else:
            st.error(res.json())

# ---------------- TEACHERS ----------------
elif menu == "Teachers":

    st.markdown('<p class="title">👨‍🏫 Teachers</p>', unsafe_allow_html=True)

    data = fetch(f"{BASE_URL}/teachers")
    st.dataframe(data, use_container_width=True)

# ---------------- SUBJECTS (UPDATED WITH TNAME) ----------------
elif menu == "Subjects":

    st.markdown('<p class="title">📚 Subjects</p>', unsafe_allow_html=True)

    data = fetch(f"{BASE_URL}/subjects")
    st.dataframe(data, use_container_width=True)

    st.subheader("📘 Subjects by Teacher Name")

    teachers = fetch(f"{BASE_URL}/teachers")
    teacher_names = [t["tname"] for t in teachers]

    tname = st.selectbox("Select Teacher Name", teacher_names)

    if st.button("Fetch Subjects"):

        teacher = next((t for t in teachers if t["tname"] == tname), None)

        if not teacher:
            st.error("Teacher not found")
        else:
            tname = teacher["tname"]

            res = requests.get(f"{BASE_URL}/teachers/{tname}/subjects")

            if res.status_code == 200:
                data = res.json()

                st.success(f"Teacher: {data['teacher_name']}")

                for sub in data["subjects"]:
                    st.markdown(f"""
                    <div class="card">
                        <h4>📘 Subject Set</h4>
                        <p><b>Sub1:</b> {sub['sub1']}</p>
                        <p><b>Sub2:</b> {sub['sub2']}</p>
                        <p><b>Sub3:</b> {sub['sub3']}</p>
                    </div>
                    """, unsafe_allow_html=True)

            else:
                st.error(res.json())