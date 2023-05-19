import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import requests
import os

owner = 'chandu11feb'
repo_name = 'Streamlit_Dashboard'


try:
    # Make a request to the GitHub API to get the list of all folders in the repository
    response = requests.get(f'https://api.github.com/repos/{owner}/{repo_name}/contents')

except:
    st.markdown('<span style="color: red;">Failed to retrieve the Excel sheet from the git repository. </span>',
                unsafe_allow_html=True)
folder_names=[]
for item12 in response.json():
    item_list=list(item12.values())
    if item_list[8] == 'dir':
        folder_names.append(item_list[0])
# Print the folder names
# print(folder_names)

release_list=[None]
sku_list=[None]
for i in folder_names:
    folder=i.split("_")
    if folder[0] not in release_list:
        release_list.append(folder[0])
    if folder[1] not in sku_list:
        sku_list.append(folder[1])


st.set_page_config(layout='wide', initial_sidebar_state='expanded')
st.title("EC Telemetry Analysis")

st.sidebar.header('Dashboard')

st.sidebar.subheader('Select Release')
release=st.sidebar.selectbox('',release_list)

st.sidebar.subheader('Select SKU')
sku=st.sidebar.selectbox('',sku_list)

submit_button=st.sidebar.button("submit")

st.sidebar.markdown("EC on-board: Microchip")


def show_warning_popup():
    st.markdown("""
        <script>
            function showPopup() {
                alert('Please Select Release and SKU ');
            }
        </script>
        """)

if release == None and sku == None:
    st.markdown('<span style="color: red;">Please Select Release and SKU </span>', unsafe_allow_html=True)
elif release == None:
    st.markdown('<span style="color: red;">Please Select Release</span>', unsafe_allow_html=True)
elif sku == None:
    st.markdown('<span style="color: red;">Please Select SKU </span>', unsafe_allow_html=True)
else:
    combination = release + "_" + sku
    st.subheader(combination)
    if combination in folder_names:
        try:
            # Set the repository owner, repository name, and the file path of the Excel sheet in the GitHub repository
            owner = 'chandu11feb'
            repo_name = 'Streamlit_Dashboard'

            file_path = combination + '/Rtsaca.xlsx'
            # Make a request to the GitHub API to get the raw content of the Excel sheet
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            thread_sheet = pd.read_excel(content_url)

            file_path = combination + '/static_ram.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            static_ram_sheet = pd.read_excel(content_url)

            file_path = combination + '/Flash_memory_usage.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            flash_memory_sheet = pd.read_excel(content_url)

            file_path = combination + '/compare_stack_usage_across_EC_FW_release.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            compare_stack_usage_sheet = pd.read_excel(content_url)

            file_path = combination + '/data_structure_holes.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            data_structure_holes_sheet = pd.read_excel(content_url)

            file_path = combination + '/worst_case_stack_req.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            worst_case_stack_sheet = pd.read_excel(content_url)

            file_path = combination + '/EC_power_consumption.xlsx'
            github_url = f'https://api.github.com/repos/{owner}/{repo_name}/contents/{file_path}'
            response1 = requests.get(github_url)
            content_url = response1.json().get('download_url')
            EC_power_consumption_sheet = pd.read_excel(content_url)

        except:
            st.markdown('<span style="color: red;">Failed to retrieve the Excel sheet from the repository. </span>', unsafe_allow_html=True)

        thread_sheet_list = thread_sheet.values.tolist()
        # print(thread_sheet_list)
        thread_rows = []
        stack_usage_list = []
        stack_allocated_list = []
        for i in thread_sheet_list:
            thread_rows.append(i[0])
            stack_usage_list.append(i[1])
            stack_allocated_list.append(i[2])
        bar_positions = range(len(thread_rows))

        # Set the width of each bar
        bar_width = 0.3

        # Plot the clustered column chart
        plt.bar(bar_positions, stack_usage_list, width=bar_width, label='Stack Usage', data="ccc")
        plt.bar([p + bar_width for p in bar_positions], stack_allocated_list, width=bar_width, label='Stack Allocated')

        # Set the x-axis labels
        plt.xticks([p + bar_width for p in bar_positions], thread_rows)

        # Add a legend( each bar details in corner)
        plt.legend()

        # Set the chart title and axes labels
        plt.title('Stack Usage v/s Stack Allocated')
        plt.xlabel('Threads')
        plt.ylabel('Values')

        # row1
        c1, c2, c3 = st.columns(3)
        with c1:
            st.markdown('### Runtime thread stack and CPU Usage Analysis')
            st.table(thread_sheet)
        with c2:
            st.markdown('### Stack Usage v/s Stack Allocated')
            st.pyplot(plt)  # clustered column chart
        with c3:
            st.markdown('### CPU Utilization v/s Time')
        # row2
        c4, c5 = st.columns(2)
        with c4:
            st.markdown('### Static RAM / Flash Memory Usage')
            st.table(static_ram_sheet)
            st.table(flash_memory_sheet)
        with c5:
            st.markdown('### Compare Stack Usage across EC FW Release')
            st.table(compare_stack_usage_sheet)
        # row3
        c6, c7, c8 = st.columns(3)
        with c6:
            st.markdown('### Data Structures holes')
            st.table(data_structure_holes_sheet)
        with c7:
            st.markdown('### Worst Case Stack Req')
            st.table(worst_case_stack_sheet)
        with c8:
            st.markdown('### EC Power Consumption')
            st.table(EC_power_consumption_sheet)
    else:
        st.markdown(
            '<span style="color: red;">Selected Release and SKU Combination Details are not Available.</span>',
            unsafe_allow_html=True)
        st.markdown(
            '<span style="color: red;">Please Select Another Release and SKU </span>',
            unsafe_allow_html=True)

## to refresh the dashboard
# refresh_interval = 25
#
# # Main app loop
# while True:
#     # Refresh the page
#     st.experimental_rerun()
#
#     # Wait for the specified interval
#     time.sleep(refresh_interval)
# st.markdown('<span style="color: red;">Please Select Release and SKU </span>', unsafe_allow_html=True)


if submit_button:
    st.experimental_rerun()

