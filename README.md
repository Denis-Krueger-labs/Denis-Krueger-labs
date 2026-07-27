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
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/decup">decup/</a></h3>
<p><code>C#</code> · <code>.NET</code> · <code>P2P Systems</code> · <code>Applied Cryptography</code></p>
<p>A decentralized peer-to-peer backup and restore prototype built as a six-person university project. It combines signed identities, peer discovery, routed messaging, chunked transfers, checksum validation, restore ownership checks, a guided terminal interface, and 352 automated tests.</p>
</td>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/Wing-FTP-CVE">wing-ftp-security-lab/</a></h3>
<p><code>Vulnerability Research</code> · <code>Exploit Validation</code> · <code>Mitigation Testing</code></p>
<p>A controlled assessment of Wing FTP Server 7.4.3 covering discovery, exploit reproduction, impact validation, and defensive testing with a reverse proxy and web application firewall.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/KMU-IT-OT-Network-Security-Lab">kmu-it-ot-network-security-lab/</a></h3>
<p><code>Network Security</code> · <code>IT/OT Segmentation</code> · <code>Lab Architecture</code></p>
<p>A practical lab for a mixed IT and operational-technology environment, documenting architecture, trust boundaries, segmentation strategy, security controls, and defensive design decisions.</p>
</td>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/Road-To-CWES">road-to-cwes/</a> · <a href="https://denis-krueger-labs.github.io/Road-To-CWES/">live</a></h3>
<p><code>Offensive Security</code> · <code>Web Exploitation</code> · <code>Learning Journal</code></p>
<p>A public learning journal combining practical labs, study logs, reusable templates, and the reasoning behind each technique rather than recording commands without context.</p>
</td>
</tr>
<tr>
<td width="50%" valign="top">
<h3><a href="https://github.com/Denis-Krueger-labs/llm-prompt-injection-paper">llm-prompt-injection-paper/</a></h3>
<p><code>Security Research</code> · <code>LLM Security</code> · <code>Academic Writing</code></p>
<p>A seminar paper examining prompt-injection vulnerabilities, current defence approaches, and the underlying instruction/data boundary problem in LLM-integrated systems.</p>
</td>
<td width="50%" valign="top">
<h3><a href="https://denis-krueger-labs.github.io/Portfolio/">portfolio/</a> · <a href="https://github.com/Denis-Krueger-labs/Portfolio">source</a></h3>
<p><code>React</code> · <code>TypeScript</code> · <code>Vite</code> · <code>Design Systems</code></p>
<p>A custom-built portfolio presenting security work, software projects, research, and learning progress through a deliberately non-corporate terminal-inspired interface.</p>
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
<td width="50%" valign="top"><h3>next-transmission/</h3><p>More security tooling, infrastructure experiments, home-lab work, and technical documentation are currently in development.</p></td>
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

<strong>Languages</strong><br>
<code>python</code> <code>c</code> <code>csharp</code> <code>bash</code> <code>java</code> <code>sql</code> <code>typescript</code>

<br><br><strong>Security</strong><br>
<code>kali</code> <code>burpsuite</code> <code>nmap</code> <code>gobuster</code> <code>ffuf</code> <code>sqlmap</code> <code>metasploit</code> <code>wireshark</code> <code>owasp-zap</code>

<br><br><strong>Systems &amp; Development</strong><br>
<code>linux</code> <code>git</code> <code>github-actions</code> <code>dotnet</code> <code>react</code> <code>vite</code> <code>docker</code> <code>proxmox</code>
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
  <a href="https://denis-krueger-labs.github.io/Portfolio/">portfolio/</a> ·
  <a href="https://denis-krueger-labs.github.io/Road-To-CWES/">road-to-cwes/</a> ·
  <a href="https://github.com/Denis-Krueger-labs/writeups">writeups/</a> ·
  <a href="https://tryhackme.com/p/0N1S3C">tryhackme/</a> ·
  <a href="https://app.hackthebox.com/public/users/3188353">hack-the-box/</a>
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
