import streamlit as st
import sqlite3
import sqlite3

st.title("📌 AI-Based To-Do List")

# ➤ **Connect to SQLite**
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

# Create user-specific tasks table
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,  -- 🆕 Store username
        task TEXT NOT NULL,
        priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')) DEFAULT 'Medium',
        deadline TEXT,
        time TEXT,  
        status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending'
    )
''')
conn.commit()

# ➤ **Ask for Username**
user = st.text_input("Enter your username:", key="username")
if not user:
    st.warning("⚠️ Please enter your username to continue.")
    st.stop()  # Stop execution if username is not provided

# ➤ **Show Saved Tasks for the User**
with st.expander("📋 See Your Tasks"):
    c.execute("SELECT * FROM tasks WHERE user=?", (user,))
    tasks = c.fetchall()

    if tasks:
        for task in tasks:
            col1, col2, col3 = st.columns([4, 1, 1])
            with col1:
                st.write(f"📝 **{task[1]}** | 🔥 `{task[2]}` | 📅 `{task[3]}` | ⏳ `{task[5]}` | ✅ `{task[4]}`")
            with col2:
                if st.button("✅ Complete", key=f"comp{task[0]}"):
                    c.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task[0],))
                    conn.commit()
                    st.rerun()
            with col3:
                if st.button("🗑️ Delete", key=f"del{task[0]}"):
                    c.execute("DELETE FROM tasks WHERE id=?", (task[0],))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No tasks available.")

# ➤ **Clear All Tasks for the Current User**
if st.button("🗑️ Clear My Tasks"):
    c.execute("DELETE FROM tasks WHERE user=?", (user,))
    conn.commit()
    st.warning("⚠️ All your tasks have been deleted!")
    st.rerun()

# ➤ **Expander for Adding a New Task**
with st.expander("➕ Add a New Task"):
    if "task_input" not in st.session_state:
        st.session_state.task_input = ""

    task = st.text_input("Task Name", value=st.session_state.task_input, key="task_box")
    pri = st.selectbox("Priority", ["High", "Medium", "Low"])
    deadline = st.date_input("Deadline")
    time = st.time_input("Deadline time")

    if st.button("✅ Add Task"):
        if not task.strip():
            st.error("⚠️ Task name cannot be empty!")
        else:
            c.execute("INSERT INTO tasks (user, task, priority, deadline, time, status) VALUES (?, ?, ?, ?, ?, 'Pending')",
                      (user, task, pri, str(deadline), str(time)))
            conn.commit()
            st.success("✅ Task Added Successfully!")

            # Reset text input field
            st.session_state.task_input = ""
            st.rerun()  # Refresh UI after adding a task

conn.close()  # Close the connection properly
