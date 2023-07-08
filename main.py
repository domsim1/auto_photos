import cv2
import time

CAPTURE_TIMER = 3600 # photos per second
PHOTOS_TO_TAKE = 12 # how many photos to take before ending
RETRY_LIMIT = 3

def main():
    taken_photos = 0
    time_from_last_photo = CAPTURE_TIMER # seconds
    is_paused = True
    retry_count = 0

    cam = cv2.VideoCapture(0)
    cv2.namedWindow("cam")

    start_time = time.time()
    last_time = start_time

    while taken_photos < PHOTOS_TO_TAKE:
        dt = start_time - last_time
        last_time = start_time
        start_time = time.time()
        ret, frame = cam.read()
        if not ret:
            print("could not get frame!!")
            if retry_count >= RETRY_LIMIT:
                break
            retry_count += 1
        if retry_count > 0:
            retry_count = 0

        frame = cv2.flip(frame, 1)
        v_frame = frame.copy()
        cv2.putText(
                v_frame,
                "time to next photo: {}".format(CAPTURE_TIMER - time_from_last_photo),
                (10, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (255, 0, 255),
                2,
                cv2.LINE_AA)
        cv2.imshow("cam", v_frame)

        k = cv2.waitKey(1)
        if k%256 == 27:
            # ESC pressed
            print("ESC pressed; closing ...")
            break
        elif k%256 == 32:
            # SPACE pressed
            is_paused = not is_paused

        if is_paused:
            continue

        time_from_last_photo += dt

        if time_from_last_photo > CAPTURE_TIMER:
            time_from_last_photo = 0
            t = time.localtime()
            t_string = time.strftime("%H-%M-%S", t)
            img_name = "pic_{}_{}.png".format(taken_photos, t_string)
            cv2.imwrite(img_name, frame)
            print("saved: {}".format(img_name))
            taken_photos += 1

        if taken_photos >= PHOTOS_TO_TAKE:
            break

    cam.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()

