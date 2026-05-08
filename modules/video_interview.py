import cv2
import time
import streamlit as st

def start_interview_recording(duration=20):

    cap = cv2.VideoCapture(0)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('final_interview_video.avi', fourcc, 20.0, (width, height))

    frame_placeholder = st.empty()
    timer_placeholder = st.empty()

    start_time = time.time()

    frames = []

    while cap.isOpened():

        ret, frame = cap.read()
        if not ret:
            break

        frames.append(frame)
        out.write(frame)

        # Show webcam frame
        frame_placeholder.image(frame, channels="BGR")

        elapsed = time.time() - start_time
        remaining = int(duration - elapsed)

        timer_placeholder.metric("⏱ Time Remaining", max(remaining,0))

        if remaining <= 0:
            break

        # Small delay so UI updates correctly
        time.sleep(0.03)

    cap.release()
    out.release()

    st.success("Answer recording finished")

    return frames