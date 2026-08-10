<p align="center">
  <img src="./assets/header.svg" alt="Denis Krüger profile terminal" width="100%" />
</p>

## `01 // IDENTITY`

```text
root@portfolio:~$ whoami
```

Information Security student at THWS Würzburg with a focus on offensive security, secure software engineering, and systems that become more interesting precisely where their assumptions begin to fail.

I care less about collecting shells than understanding the broken assumption that made them possible, how the weakness can be reproduced, and what a real fix should look like.

```text
current signal  building security tools
                documenting labs
                expanding the home lab
                working toward deeper offensive-security practice
```

---

## `02 // PROJECT ARCHIVE`

```text
root@portfolio:~$ ls ~/projects
```
<table>

<tr>
<td colspan="2" valign="top">
<h3><a href="https://denis-krueger-labs.github.io/Portfolio/">portfolio/</a> · <a href="https://github.com/Denis-Krueger-labs/Portfolio">source</a></h3>
<p><code>React</code> · <code>TypeScript</code> · <code>Vite</code> · <code>Design Systems</code></p>
<p>A custom-built portfolio presenting security work, software projects, research, and learning progress through a deliberately non-corporate terminal-inspired interface.</p>
</td>
</tr>

<tr>
<td colspan="2" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/home-lab">home-lab/</a></h3>
<p><code>Proxmox</code> · <code>OPNsense</code> · <code>Active Directory</code> · <code>NixOS</code> · <code>Infrastructure Security</code></p>
<p>A documented small enterprise-style security lab built on Proxmox VE with an isolated OPNsense network, Windows Server 2025 Active Directory, a domain-joined Windows 11 client, reusable Debian and Windows templates, backup and remote-access paths, and the experimental NixOS and Hyprland Mori OS workstation.</p>
</td>
</tr>

<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/Wing-FTP-CVE">wing-ftp-security-lab/</a></h3>
<p><code>Vulnerability Research</code> · <code>Exploit Validation</code> · <code>Mitigation Testing</code></p>
<p>A controlled assessment of Wing FTP Server 7.4.3 covering discovery, exploit reproduction, impact validation, and defensive testing with a reverse proxy and web application firewall.</p>
</td>

<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/copy-fail-lab">copyfail-security-lab/</h3>
<p><code>Linux Kernel</code> · <code>Privilege Escalation</code> · <code>Detection Engineering</code></p>
<p>A controlled reproduction of CopyFail examining a Linux kernel local privilege escalation from exploit validation and root-cause analysis through behavioural detection, mitigation, and patch validation.</p>
</td>
</tr>

<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/decup">decup/</a></h3>
<p><code>C#</code> · <code>.NET</code> · <code>P2P Systems</code> · <code>Applied Cryptography</code></p>
<p>A decentralized peer-to-peer backup and restore prototype built as a six-person university project. It combines signed identities, peer discovery, routed messaging, chunked transfers, checksum validation, restore ownership checks, a guided terminal interface, and 352 automated tests.</p>
</td>

<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/KMU-IT-OT-Network-Security-Lab">kmu-it-ot-network-security-lab/</a></h3>
<p><code>Network Security</code> · <code>IT/OT Segmentation</code> · <code>Lab Architecture</code></p>
<p>A practical lab for a mixed IT and operational-technology environment, documenting architecture, trust boundaries, segmentation strategy, security controls, and defensive design decisions.</p>
</td>
</tr>

<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/Road-To-CWES">road-to-cwes/</a> · <a href="https://denis-krueger-labs.github.io/Road-To-CWES/">live</a></h3>
<p><code>Offensive Security</code> · <code>Web Exploitation</code> · <code>Learning Journal</code></p>
<p>A public learning journal combining practical labs, study logs, reusable templates, and the reasoning behind each technique rather than recording commands without context.</p>
</td>

<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/llm-prompt-injection-paper">llm-prompt-injection-paper/</a></h3>
<p><code>Security Research</code> · <code>LLM Security</code> · <code>Academic Writing</code></p>
<p>A seminar paper examining prompt-injection vulnerabilities, current defence approaches, and the underlying instruction/data boundary problem in LLM-integrated systems.</p>
</td>
</tr>


</table>

---

## `03 // ADDITIONAL BUILDS`

```text
root@portfolio:~$ find ~/projects -maxdepth 1 -type d
```

<table>
<tr>
<td width="50%" valign="top"><h3><a href="https://github.com/Denis-Krueger-labs/pwgen-lite">pwgen-lite/</a></h3><p>Python password generator using <code>secrets</code>, HMAC-SHA256, rejection sampling, entropy estimates, and tests.</p></td>
<td width="50%" valign="top"><h3><a href="https://github.com/Denis-Krueger-labs/mfind">mfind/</a></h3><p>C implementation of a simplified Unix <code>find</code> with recursive traversal, filters, optional POSIX threads, and Valgrind verification.</p></td>
</tr>
<tr>
<td width="50%" valign="top"><h3><a href="https://github.com/Denis-Krueger-labs/writeups">writeups/</a></h3><p>Structured Hack The Box and TryHackMe reports covering recon, exploitation, privilege escalation, evidence, and defensive context.</p></td>
<td width="50%" valign="top"><h3><a href="https://github.com/Denis-Krueger-labs/fixdesk">fixdesk/</a></h3><p>React and TypeScript repair-shop frontend with customer, device, and repair-order workflows.</p></td>
</tr>
<tr>
<td width="50%" valign="top"><h3><a href="https://github.com/Denis-Krueger-labs/blue.">blue./</a></h3><p>Editorial-brutalist React festival site with responsive layouts, motion, theme switching, and custom visual design.</p></td>
<td width="50%" valign="top"><h3>next-transmission/</h3><p>More security tooling, infrastructure experiments, and technical documentation are currently in development.</p></td>
</tr>
</table>

---

<table>
<tr>
<td width="50%" valign="top">
<h2><code>04 // METHODOLOGY</code></h2>

```text
root@portfolio:~$ cat methodology.md

Reconnaissance
→ Enumeration
→ Vulnerability identification
→ Exploitation and validation
→ Privilege escalation
→ Root-cause analysis
→ Remediation and documentation
```

The goal is not merely to prove that something breaks, but to explain why it breaks, what assumption failed, how the finding can be reproduced safely, and how the weakness should be fixed.
</td>
<td width="50%" valign="top">
<h2><code>05 // INSTALLED PACKAGES</code></h2>

```text
root@portfolio:~$ pacman -Q
```

````html
<td width="50%" valign="top">
<h2><code>05 // INSTALLED PACKAGES</code></h2>

```text
root@portfolio:~$ pacman -Q
````

<strong>Languages</strong><br>

<img src="https://img.shields.io/badge/Python-161a20?style=flat-square&logo=python&logoColor=a878e3" alt="Python" />
<img src="https://img.shields.io/badge/C-161a20?style=flat-square&logo=c&logoColor=a878e3" alt="C" />
<img src="https://img.shields.io/badge/C%23-161a20?style=flat-square&logo=dotnet&logoColor=a878e3" alt="C#" />
<img src="https://img.shields.io/badge/Bash-161a20?style=flat-square&logo=gnubash&logoColor=a878e3" alt="Bash" />
<img src="https://img.shields.io/badge/Java-161a20?style=flat-square&logo=openjdk&logoColor=a878e3" alt="Java" />
<img src="https://img.shields.io/badge/SQL-161a20?style=flat-square" alt="SQL" />
<img src="https://img.shields.io/badge/TypeScript-161a20?style=flat-square&logo=typescript&logoColor=a878e3" alt="TypeScript" />

<strong>Security</strong><br>

<img src="https://img.shields.io/badge/Kali%20Linux-161a20?style=flat-square&logo=kalilinux&logoColor=a878e3" alt="Kali Linux" />
<img src="https://img.shields.io/badge/Burp%20Suite-161a20?style=flat-square&logo=portswigger&logoColor=a878e3" alt="Burp Suite" />
<img src="https://img.shields.io/badge/Nmap-161a20?style=flat-square&logo=gnometerminal&logoColor=a878e3" alt="Nmap" />
<img src="https://img.shields.io/badge/Gobuster-161a20?style=flat-square&logo=gnometerminal&logoColor=a878e3" alt="Gobuster" />
<img src="https://img.shields.io/badge/ffuf-161a20?style=flat-square&logo=gnometerminal&logoColor=a878e3" alt="ffuf" />
<img src="https://img.shields.io/badge/sqlmap-161a20?style=flat-square&logo=gnometerminal&logoColor=a878e3" alt="sqlmap" />
<img src="https://img.shields.io/badge/Metasploit-161a20?style=flat-square&logo=metasploit&logoColor=a878e3" alt="Metasploit" />
<img src="https://img.shields.io/badge/Wireshark-161a20?style=flat-square&logo=wireshark&logoColor=a878e3" alt="Wireshark" />
<img src="https://img.shields.io/badge/OWASP%20ZAP-161a20?style=flat-square&logo=owasp&logoColor=a878e3" alt="OWASP ZAP" />

<strong>Systems & Development</strong><br>

<img src="https://img.shields.io/badge/Linux-161a20?style=flat-square&logo=linux&logoColor=a878e3" alt="Linux" />
<img src="https://img.shields.io/badge/Git-161a20?style=flat-square&logo=git&logoColor=a878e3" alt="Git" />
<img src="https://img.shields.io/badge/GitHub%20Actions-161a20?style=flat-square&logo=githubactions&logoColor=a878e3" alt="GitHub Actions" />
<img src="https://img.shields.io/badge/.NET-161a20?style=flat-square&logo=dotnet&logoColor=a878e3" alt=".NET" />
<img src="https://img.shields.io/badge/React-161a20?style=flat-square&logo=react&logoColor=a878e3" alt="React" />
<img src="https://img.shields.io/badge/Vite-161a20?style=flat-square&logo=vite&logoColor=a878e3" alt="Vite" />
<img src="https://img.shields.io/badge/Docker-161a20?style=flat-square&logo=docker&logoColor=a878e3" alt="Docker" />
<img src="https://img.shields.io/badge/Proxmox-161a20?style=flat-square&logo=proxmox&logoColor=a878e3" alt="Proxmox" />
<img src="https://img.shields.io/badge/OPNsense-161a20?style=flat-square&logo=opnsense&logoColor=a878e3" alt="OPNsense" />
<img src="https://img.shields.io/badge/NixOS-161a20?style=flat-square&logo=nixos&logoColor=a878e3" alt="NixOS" />

<img src="https://img.shields.io/badge/Active%20Directory-161a20?style=flat-square&logo=data:image/svg%2Bxml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHZpZXdCb3g9IjAgMCAyNCAyNCI%2BPHBhdGggZmlsbD0iI2E4NzhlMyIgZD0iTTIgNC40IDEwLjIgM3Y4SDJWNC40Wm05LjItMS42TDIyIDF2MTBIMTEuMlYyLjhaTTIgMTJoOC4ydjhMMiAxOC42VjEyWm05LjIgMEgyMnYxMGwtMTAuOC0xLjhWMTJaIi8%2BPC9zdmc%2B" alt="Active Directory" />

<img src="https://img.shields.io/badge/Tailscale-161a20?style=flat-square&logo=tailscale&logoColor=a878e3" alt="Tailscale" />

</td>
```


</td>
</tr>
</table>

---

## `06 // JOURNALCTL`

```text
root@portfolio:~$ journalctl --since "365 days ago"
```

<p align="center">
  <img src="./assets/activity.svg" alt="GitHub contribution activity for the last 365 days" width="100%" />
</p>


[![GitHub Streak](https://streak-stats.demolab.com?user=Denis-Krueger-labs&theme=dark&timezone=%2B2&date_format=j%2Fn%5B%2FY%5D&card_width=1100&ring=A878E3&border=3B2B4F&stroke=3B2B4F&currStreakNum=E8DFCF&fire=A878E3&sideNums=E8DFCF&sideLabels=877C91&dates=9B6FD3&currStreakLabel=9B6FD3&excludeDaysLabel=877C91&background=0B0D10&hide_total_contributions=true)](https://git.io/streak-stats)

<table>
<tr>
<td width="50%" align="center" valign="middle"><a href="https://tryhackme.com/p/0N1S3C"><img src="https://tryhackme-badges.s3.amazonaws.com/0N1S3C.png" alt="TryHackMe profile badge" width="100%" /></a></td>
<td width="50%" align="center" valign="middle"><a href="https://app.hackthebox.com/public/users/3188353"><img src="https://www.hackthebox.eu/badge/image/3188353" alt="Hack The Box profile badge" width="100%" /></a></td>
</tr>
</table>



---

## `07 // KNOWN ROUTES`

```text
root@portfolio:~$ ls ~/known-routes
```

<p align="center">
  <a href="YOUR-LINKEDIN-URL">
    <img src="https://img.shields.io/badge/LINKEDIN-CONNECT-9d4dff?style=for-the-badge&logo=linkedin&logoColor=f4f0ff&labelColor=18171c" alt="LinkedIn" />
  </a>

  <a href="https://profile.hackthebox.com/profile/019c7d76-1e97-73d7-90de-5861d7eb8087">
    <img src="https://img.shields.io/badge/HACK_THE_BOX-0N1S3C-9d4dff?style=for-the-badge&logo=hackthebox&logoColor=f4f0ff&labelColor=18171c" alt="Hack The Box" />
  </a>

  <a href="https://tryhackme.com/p/0N1S3C">
    <img src="https://img.shields.io/badge/TRYHACKME-0N1S3C-9d4dff?style=for-the-badge&logo=tryhackme&logoColor=f4f0ff&labelColor=18171c" alt="TryHackMe" />
  </a>

</p>


---

<p align="center">
  <img src="./assets/footer.svg" alt="Terminal footer" width="100%" />
</p>

<!--
curiosity survives containment
systems reveal themselves to those who keep asking why
information wants to be free
-->



