# ansible-vscode
vscode on ubuntu ... kept up to date with ansible-pull

```bash
curl -fsSL https://raw.githubusercontent.com/rhildred/ansible-vscode/main/bootstrap|bash
```
## To add oauth2 proxy.

Generate a cookie_secret by running python3 -c "import random, string; print(''.join(random.choices(string.ascii_uppercase + string.digits, k=32)))"
Edit /etc/oauth2-proxy.cfg to have your_github_client_id, your_github_client_secret and your_cookie_secret the way you need them.
Edit /etc/systemd/system/oauth2-proxy.service to have github_usernames_separated_by_commas the way you need it.
run sudo systemctl enable oauth2-proxy.service
run sudo systemctl start oauth2-proxy.service
Now you should be able to login to your instance from the internet with your github credentials.
