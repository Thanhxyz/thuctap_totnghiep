import streamlit as st
import psycopg2

DB_URL = "postgresql://neondb_owner:npg_puzIOU3Y5VET@ep-bitter-cloud-a8dztndt-pooler.eastus2.azure.neon.tech/neondb?sslmode=require"

@st.cache_resource
def get_connection():
    try:
        conn = psycopg2.connect(DB_URL)
        return conn
    except psycopg2.Error as e:
        st.error(f"Lỗi kết nối database: {e}")
        return None

def execute_query(query, params=(), fetch=False):
    conn = get_connection()
    if conn is None:
        return None
    
    try:
        with conn.cursor() as cursor:
            cursor.execute(query, params)
            conn.commit()
            if fetch:
                return cursor.fetchall()
    except psycopg2.Error as e:
        st.error(f"Lỗi khi thực hiện query: {e}")
        return None

def get_next_id(table_name, id_column):
    query = f"SELECT COALESCE(MAX({id_column}), 0) + 1 FROM {table_name}"
    result = execute_query(query, fetch=True)
    return result[0][0] if result else 1

def check_project_exists(project_id):
    query = "SELECT 1 FROM project_info WHERE project_id = %s"
    result = execute_query(query, (project_id,), fetch=True)
    return result is not None and len(result) > 0

def add_project(project_name, total_supply, launch_date, category, website):
    project_id = get_next_id("project_info", "project_id")
    query = """
        INSERT INTO project_info (project_id, project_name, total_supply, launch_date, category, website)
        VALUES (%s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (project_id, project_name, total_supply, launch_date, category, website))
    st.success(f"Dự án '{project_name}' đã được thêm thành công!")

def update_project(project_id, project_name, total_supply, launch_date, category, website):
    if not check_project_exists(project_id):
        st.error("Dự án không tồn tại!")
        return
    
    query = """
        UPDATE project_info SET project_name = %s, total_supply = %s, launch_date = %s, category = %s, website = %s
        WHERE project_id = %s
    """
    execute_query(query, (project_name, total_supply, launch_date, category, website, project_id))
    st.success("Cập nhật dự án thành công!")

def add_token_allocation(project_id, category, percentage, cliff_months, vesting_months, initial_unlock):
    if not check_project_exists(project_id):
        st.error("Dự án không tồn tại!")
        return
    
    allocation_id = get_next_id("token_allocation", "allocation_id")
    query = """
        INSERT INTO token_allocation (allocation_id, project_id, category, percentage, cliff_months, vesting_months, initial_unlock)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    execute_query(query, (allocation_id, project_id, category, percentage, cliff_months, vesting_months, initial_unlock))
    st.success("Thêm token allocation thành công!")

def main():
    st.title("Quản lý Dự án Crypto")
    menu = ["Thêm Project", "Chỉnh sửa Project", "Thêm Tokenomic"]
    choice = st.sidebar.selectbox("Chọn chức năng", menu)
    
    if choice == "Thêm Project":
        st.subheader("Thêm Dự án Mới")
        project_name = st.text_input("Tên dự án")
        total_supply = st.number_input("Tổng cung", min_value=0, step=1)
        launch_date = st.date_input("Ngày ra mắt")
        category = st.text_input("Danh mục")
        website = st.text_input("Website")
        
        if st.button("Thêm Dự án"):
            add_project(project_name, total_supply, launch_date, category, website)
    
    elif choice == "Chỉnh sửa Project":
        st.subheader("Chỉnh sửa Thông tin Dự án")
        project_id = st.number_input("Nhập ID dự án", min_value=1, step=1)
        project_name = st.text_input("Tên dự án mới")
        total_supply = st.number_input("Tổng cung mới", min_value=0, step=1)
        launch_date = st.date_input("Ngày ra mắt mới")
        category = st.text_input("Danh mục mới")
        website = st.text_input("Website mới")
        
        if st.button("Cập nhật Dự án"):
            update_project(project_id, project_name, total_supply, launch_date, category, website)
    
    elif choice == "Thêm Tokenomic":
        st.subheader("Thêm Thông tin Phân bổ Token")
        project_id = st.number_input("Nhập ID dự án", min_value=1, step=1)
        category = st.text_input("Danh mục Tokenomic")
        percentage = st.number_input("Phần trăm", min_value=0.0, max_value=100.0, step=0.1)
        cliff_months = st.number_input("Thời gian Cliff (tháng)", min_value=0, step=1)
        vesting_months = st.number_input("Thời gian Vesting (tháng)", min_value=0, step=1)
        initial_unlock = st.number_input("Phần trăm mở khóa ban đầu", min_value=0.0, max_value=100.0, step=0.1)
        
        if st.button("Thêm Tokenomic"):
            add_token_allocation(project_id, category, percentage, cliff_months, vesting_months, initial_unlock)

if __name__ == "__main__":
    main()
