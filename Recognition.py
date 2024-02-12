import cv2 as cv
from pyzbar.pyzbar import decode

class Recognition:
    data = []       ## found data list
    def run(self):      ## function cascade
        self.cam = self.cam_ON()
        while True:
            self.frame = self.reading()
            self.recognized = self.recognition()
            for object in self.recognized:
                self.object = object
                self.highlight()
                self.print_out()
            self.cam_out()
            if self.quit_program():
                break
        self.cam_OFF()
        self.out_data()

    def cam_ON(self):       ## connecting camera
        cam = cv.VideoCapture(0)
        # cam = cv.VideoCapture("rtsp://192.168.1.55:5005/routecam")
        return cam

    def reading(self):      ## getting frames
        ret, frame = self.cam.read()
        return frame

    def recognition(self):      ## finding QR code
        recognized = decode(self.frame)
        return recognized

    def highlight(self):        ## rectangle highlighting
        bbox = self.object.rect
        cv.rectangle(self.frame, (bbox.left, bbox.top), (bbox.left + bbox.width, bbox.top + bbox.height), (0, 255, 0), 2)

    def print_out(self):        ## data output realtime
        output = self.object.data.decode("utf-8")
        print("QR Code Data:",'\033[33m', output,'\033[0m')
        if output not in Recognition.data:
            Recognition.data.append(output)

    def cam_out(self):      ## camera output
        cv.imshow("QR Code Reader", self.frame)

    def quit_program(self):     ## program quitting
        return cv.waitKey(1) & 0xFF == ord('q')

    def cam_OFF(self):      ## disconnecting camera
        self.cam.release()
        cv.destroyAllWindows()

    def out_data(self):     ## data output print
        print("", '\033[32m')
        print("="*50)
        print("Data:", Recognition.data)
        print("Len =", len(Recognition.data))
        print("="*50, '\033[0m')

Recognition().run()