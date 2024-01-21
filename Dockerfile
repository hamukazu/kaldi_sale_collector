FROM ubuntu:23.04

RUN apt-get update -y
RUN apt-get install -y python3 python3-pip wget

RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub \
  | gpg --dearmor | tee /etc/apt/trusted.gpg.d/google.gpg >/dev/null
RUN echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list
RUN apt-get update -y
RUN apt-get -y --no-install-recommends install google-chrome-stable

RUN mkdir /work
COPY . /work
RUN chmod +x /work/wrap_chrome_binary
RUN /work/wrap_chrome_binary

WORKDIR /work
RUN pip3 install --break-system-packages --upgrade pip
RUN pip3 install --break-system-packages selenium chromedriver-autoinstaller
RUN pip3 install --break-system-packages -r requirements.txt
