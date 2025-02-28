import streamlit as st
import sqlite3

st.title("📌 AI-Based To-Do List")

# ➤ **Connect to SQLite (Prevents database locking issue)**
conn = sqlite3.connect("tasks.db", check_same_thread=False)
c = conn.cursor()

# Create tasks table if it doesn't exist
c.execute('''
    CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        task TEXT NOT NULL,
        priority TEXT CHECK(priority IN ('High', 'Medium', 'Low')) DEFAULT 'Medium',
        deadline TEXT,
        time TEXT,  
        status TEXT CHECK(status IN ('Pending', 'Completed')) DEFAULT 'Pending'
    )
''')
conn.commit()

# ➤ **Show Saved Tasks**
with st.expander("📋 See Saved Tasks"):
    c.execute("SELECT * FROM tasks")
    tasks = c.fetchall()

    if tasks:
        for task in tasks:
            col1, col2 = st.columns([4, 1])  # Create layout
            with col1:
                st.write(
                    f"📝 **{task[1]}** | 🔥 Priority: `{task[2]}` | 📅 Due Date: `{task[3]}` | ⏳ Due Time: `{task[5]}` | ✅ Status: `{task[4]}`")
                if st.button("✅ Complete", key=task[0]):
                    c.execute("UPDATE tasks SET status='Completed' WHERE id=?", (task[0],))
                    conn.commit()
                    st.rerun()

            with col2:
                if st.button("🗑️ Delete", key=f"del{task[0]}"):
                    c.execute("DELETE FROM tasks WHERE id=?", (task[0],))
                    conn.commit()
                    st.rerun()
    else:
        st.info("No tasks available.")


# ➤ **Clear All Tasks**
if st.button("🗑️ Clear All Tasks"):
    c.execute("DELETE FROM tasks")  # Deletes all rows but keeps table
    conn.commit()
    st.warning("⚠️ All tasks have been deleted!")
    st.rerun()  # Refresh UI

# ➤ **Expander for Adding a New Task**
with st.expander("➕ Add a New Task"):
    # Initialize session state for text input
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
            c.execute("INSERT INTO tasks (task, priority, deadline, time, status) VALUES (?, ?, ?, ?, 'Pending')",
                      (task, pri, str(deadline), str(time)))
            conn.commit()
            st.success("✅ Task Added Successfully!")

            # Reset text input field
            st.session_state.task_input = ""
            st.rerun()  # Refresh UI after adding a task

conn.close()  # Close the connection properly
