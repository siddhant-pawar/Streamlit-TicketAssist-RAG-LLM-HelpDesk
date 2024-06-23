import streamlit as st
import os

video_folder = "E:/mywork/helphand/chatboy/backend/uploaded_videos"

def videos():
    if not os.path.exists("uploaded_videos"):
        os.makedirs("uploaded_videos")

    st.sidebar.title("Video Upload and List App")

    # File upload section
    st.sidebar.header("Upload Video")
    uploaded_file = st.sidebar.file_uploader("Choose a video...", type=["mp4", "avi"])

    if uploaded_file is not None:
        file_extension = uploaded_file.name.split(".")[-1]
        if file_extension.lower() not in ["mp4", "avi"]:
            st.sidebar.error("Invalid file format. Please upload a .mp4 or .avi file.")
        else:
            with open(os.path.join("uploaded_videos", uploaded_file.name), "wb") as f:
                f.write(uploaded_file.read())
            st.sidebar.success("Video uploaded successfully!")

    st.header("List of Uploaded Videos")
    video_files = os.listdir("uploaded_videos")
    if not video_files:
        st.info("No videos uploaded yet.")
    else:
        for video_file in video_files:
            video_path = os.path.join("uploaded_videos", video_file)
            st.video(video_path, format='video/mp4', start_time=0)
            st.caption(video_file)

    video_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith(".mp4")]

    # Display videos in a grid pattern
    if video_files:
        st.subheader("List of Videos")
        num_columns = 5  

        num_videos = len(video_files)
        num_rows = (num_videos + num_columns - 1) // num_columns
        for i in range(num_rows):
            row_videos = video_files[i * num_columns : (i + 1) * num_columns]
            cols = st.columns(num_columns)

            for j, video_path in enumerate(row_videos):
                with cols[j]:
                    st.video(video_path, format='video/mp4', start_time=0)
                    video_name = os.path.basename(video_path)
                    st.caption(video_name)

    else:
        st.warning("No video files found in the specified folder.")




video_folder = "E:/mywork/helphand/chatboy/backend/uploaded_videos"

def show_videos():
    st.title("List of Videos")

    video_files = [os.path.join(video_folder, file) for file in os.listdir(video_folder) if file.endswith(".mp4")]

    if not video_files:
        st.warning("No video files found in the specified folder.")
    else:
        for video_path in video_files:
            try:
                video_file = open(video_path, 'rb')
                video_bytes = video_file.read()
                st.video(video_bytes, format='video/mp4', start_time=0)
                video_file.close()
                video_name = os.path.basename(video_path)
                st.caption(video_name)
            except Exception as e:
                st.error(f"Error loading video {video_path}: {str(e)}")


    