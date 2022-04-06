FROM alpine:latest

# Thank you to clubby789
# xinetd from https://github.com/DarinMao/xinetd-musl/releases/tag/xinetd-2-3-15
ENV DEBIAN_FRONTEND noninteractive
RUN apk add --no-cache qemu-system-x86_64 && rm /usr/share/qemu/*.fd && rm /usr/bin/qemu-storage-daemon /usr/bin/qemu-hexagon /usr/bin/qemu-keymap /usr/bin/qemu-pr-helper /usr/bin/openssl /usr/lib/libX* && rm -rf /usr/share/X11
COPY --chown=root ./xinetd-static /usr/sbin/xinetd
RUN chmod +x /usr/sbin/xinetd
COPY challenge/xinetd.conf /etc/xinetd.conf
RUN mkdir /etc/xinetd.d

RUN addgroup -g 1000 ctf && adduser -u 1000 -G ctf -h /home/ctf -D ctf

ADD --chown=ctf challenge/initramfs_with_real_flag_only_for_server.cpio.gz /home/ctf/initramfs.cpio.gz
ADD --chown=ctf challenge/bzImage /home/ctf/bzImage
COPY --chown=ctf challenge/run.sh /home/ctf/run.sh
COPY --chown=root challenge/ka2.xinetd /etc/xinetd.d/ka2
RUN chown -R root:ctf /home/ctf
RUN echo "Slow down" > /etc/banner_fail
RUN chmod 750 /home/ctf/bzImage
RUN chmod +x /home/ctf/run.sh
EXPOSE 9999

CMD ["/usr/sbin/xinetd", "-dontfork"]