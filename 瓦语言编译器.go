package main

import (
    "bufio"
    "os"
    "os/exec"
	"time"
)

func main() {
    reader := bufio.NewReader(os.Stdin)
    income, _ := reader.ReadString('\n')
	income="123"+income
    for {
        cmd := exec.Command("python", ".\\config\\main.py")

        cmd.Stdout = os.Stdout
        cmd.Stderr = os.Stderr


        err := cmd.Run()
        if err != nil {
        } else {
        }

        // 等待 3 秒后再次执行（防止疯狂重启）
        time.Sleep(999999 * time.Second)
    }
}
