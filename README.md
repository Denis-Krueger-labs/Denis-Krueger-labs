# Hi, I'm Denis Krüger

InfoSec student at THWS Würzburg, focused on offensive security.
More interested in understanding *why* something is exploitable than just getting the shell 
the root cause, the misassumption, what a real fix would actually look like.

Currently working through HTB and THM alongside my studies, mostly web apps and Linux privesc,
with AD and network attack surfaces next on the list. Everything gets written up.

**Into:**
- Web Application Exploitation
- Linux & Windows Privilege Escalation
- Wireless & Network Attack Surface Analysis
- Embedded & IoT Security
- Active Directory

---

## Projects

### [pwgen-lite](https://github.com/Denis-Krueger-labs/pwgen-lite) Python

Minimal CLI password generator built around secure randomness and cryptographic correctness.
Implements `secrets`-based generation, HMAC-SHA256 deterministic mode with rejection
sampling to avoid modulo bias, entropy estimation, and brute-force time modelling.
Includes a full pytest suite and proper exit codes.

### [mfind](https://github.com/Denis-Krueger-labs/mfind) C

Simplified reimplementation of the Unix `find` utility, written in C as part of a
university systems programming project.
Supports recursive directory traversal, name/type/size/depth filtering, and optional
parallel traversal across start directories using POSIX threads.
Verified memory-safe with Valgrind (zero leaks).

### [LLM Prompt Injection Defences](https://github.com/Denis-Krueger-labs/llm-prompt-injection) Research

Seminar paper (THWS, SS2026) analyzing prompt injection vulnerabilities in LLM-integrated
systems and evaluating current defence mechanisms  including StruQ, SecAlign, spotlighting,
and system-level IFC approaches. Evaluated against AgentDojo, InjecAgent, and OpenPromptInjection
benchmarks. Examines the fundamental instruction/data boundary problem and the limits of
fine-tuning-based defences under adaptive attacks.

### [Road to CWES](https://github.com/Denis-Krueger-labs/road-to-cwes)  [site](https://denis-krueger-labs.github.io/Road-To-CWES/)

Public learning journal documenting progress toward the Certified Web Exploitation Specialist.
Daily study logs covering web fundamentals, HTTP/HTTPS, cURL, and practical web security
methodology. Structured to be reusable  includes templates for anyone who wants to document
their own learning journey the same way.

### [writeups](https://github.com/Denis-Krueger-labs/writeups)

Structured technical reports documenting lab-based security assessments on HackTheBox and TryHackMe.
Each writeup follows a standardized methodology covering reconnaissance, exploitation,
privilege escalation, and defensive considerations.

---

## Assessment Workflow

```
Reconnaissance → Enumeration → Vulnerability ID → Exploitation → Privesc → Documentation
```

---

## Practice Platforms

<a href="https://tryhackme.com/p/0N1S3C">
  <img src="https://tryhackme-badges.s3.amazonaws.com/0N1S3C.png"
       alt="TryHackMe Badge"
       width="350" />
</a>
<br><br>
<a href="https://app.hackthebox.com/public/users/3188353">
  <img src="https://www.hackthebox.eu/badge/image/3188353"
       alt="HackTheBox Badge"
       width="350" />
</a>

---

## Tools & Technologies

**Languages:** Python · C · C# · Bash · Java · SQL  
**Security:** Kali Linux · Burp Suite · Nmap · Gobuster · ffuf · SQLMap · Metasploit · Wireshark · OWASP ZAP 
**Systems:** Linux · Git · .NET

---

> ᓚ₍⑅^..^₎♡ just enumerating quietly
