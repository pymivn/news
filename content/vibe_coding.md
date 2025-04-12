title: Flashcard luyện thi chứng chỉ
date: 2025-04-12
tags: Python, vibe_coding, roocode, gemini
category: pymi.vn
slug: vibe_coding
authors: thevix
description: Tạo webapp flashcard để luyện thi chứng chỉ trong 15 phút!

### Context (Rất quan trọng cho cả người đọc và LLM)
Tác giả đang trong thời gian ôn luyện để thi chứng chỉ AWS và GCP nên đã tìm tới các exam dump để làm quen với đề. Tuy nhiên, các trang này không đem lại trải nghiệm học tập tốt lắm:
- Hiển thị 1 lúc nhiều câu hỏi, ít nhất là 5
- Khi sang trang mới cần phải chứng minh mình không phải là người máy
- Muốn đánh dấu 1 câu hỏi khó để xem lại hoặc thêm ghi chú thì phải dùng 1 spreadsheet riêng để track
- Vân vân..

Vì vậy, tác giả đã quyết định tự làm 1 web app riêng để thoả mãn sự khó tính của bản thân. Để tiết kiệm thời gian, nếu không sẽ bị mất tinh thần học tập, tác giả đã `Vibe coding` cùng model `Gemini Pro 2.5`.

Các công cụ mà tác giả như sau:
- VS Code
- Roo Code (VS Code plugin)
- Openrouter: Model Gemini Pro 2.5 free (10 limits per day) 
- AI Studio: Model Gemini Pro 2.5 API free (10 limits per day)

### Vibe coding là gì?
Theo wikipedia định nghĩa là: Code cùng với AI. Mình ra lệnh cho LLM, mình kiểm tra đầu ra, nếu đúng kết quả như mình mong muốn thì lưu file lại. Cứ như thế lặp đi lặp lại.
>Vibe coding (also vibecoding) is an AI-dependent programming technique where a person describes a problem in a few sentences as a prompt to a large language model (LLM) tuned for coding. The LLM generates software, shifting the programmer's role from manual coding to guiding, testing, and refining the AI-generated source code. Vibe coding is claimed by its advocates to allow even amateur programmers to produce software without the extensive training and skills required for software engineering. The term was introduced by Andrej Karpathy in February 2025 and listed in the Merriam-Webster Dictionary the following month as a "slang & trending" noun.

Giờ thì vào việc thôi.

### Hiểu rõ và phát thảo sơ bộ Web App sẽ như thế nào
Đây là toàn bộ prompt đầu tiên của tác giả. Nôm na là:
1. Mô tả công nghệ
- Viết 1 Python web app
- App này được gói trong 1 container, để khi dùng chỉ cần docker up
- Viết app này bằng django hay flaskr gì cũng được, miễn là dễ maintain

2. Mô tả tính năng
- Dùng sqlite3 để lưu data cho toàn bộ webapp
- Database này sẽ lưu dữ liệu câu hỏi, câu trả lời và câu trả lời đúng
- Người dùng sẽ cung cấp 1 file csv để import bộ dữ liệu này
- Người dùng có thể thêm nhiều bộ câu hỏi cho từng loại chứng chỉ khác nhau
- Vân vân...

[Link dễ xem hơn](https://github.com/thevivotran/studytest/blob/main/idea/1/idea_draft.md)

```
I want to develop python webapp that can run in every users local machine. the app is packaged in a container, so everyone will be able to docker up it (or podman up it). the app can be writen in django or flask, or what ever framework that easy to maintain in the future.

the webapp's name is "Flashcard", this is a flashcard app. this app will have a database (sqlite3). this database stores questions, answers and correct answer of the question. each question has only 1 correct answer. the database will be initiated at every first run. at first, user will provide a csv file that have 7 columns and a name for the dataset:
- question
- correct answer
- answer choice 1
- answer choice 2
- answer choice 3
- answer choice 4
- answer choice 5 (optional)

when successfuly inject data into sqlite3 database, user will be able to choose between dataset to learn. after selecting a desired dataset, user will be moved to a flashcards feature. 

in the flashcards feature, user will be able to go through all the questions by swiping the flashcard. at each flashcard, user will always see the question and 4 (or 5) answers will be listed out at first, when tap to the flashcard, the correct answer will be showed.

in the flashcards feature, the learning progress will be cached for each dataset. whenever user choose the dataset to learn, the flashcards will resume at the last learning.

in the flashcards feature, user will be able to get back to the choose dataset page.
```

### Dùng tính năng chi tiết hoá prompt
`Roo Code` có 1 tính năng là dùng AI để chi tiết hoá prompt đầu vào của người dùng. Prompt càng chi tiết thì các Model càng dễ hiểu và trả ra kết quả cũng chính xác hơn.

Bên dưới đây là 10 dòng đầu của đoạn prompt đã được bổ sung thêm thông tin ([Toàn bộ file](https://github.com/thevivotran/studytest/blob/main/idea/1/enhanced_idea_draft.md)):
```
Develop a Python web application named "Flashcard", designed to run locally on user machines via Docker or Podman. Use the Flask framework and SQLite3 for the database.

**Core Requirements:**

1.  **Containerization:** Package the application in a Docker container. Provide a `Dockerfile` using a Python base image (e.g., `python:3.10-slim`), a `requirements.txt` file (including Flask), and instructions for building and running the container, ensuring data persistence via volume mounting for the database and user progress. The application should be accessible via a mapped port (e.g., 5000).
2.  **Database (`flashcard.db`):**
    *   Use SQLite3, stored within the persistent volume (`/data/flashcard.db`).
    *   Schema:
        *   `datasets` table: `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `name` (TEXT UNIQUE NOT NULL).
        *   `cards` table: `id` (INTEGER PRIMARY KEY AUTOINCREMENT), `dataset_id` (INTEGER, FOREIGN KEY (`dataset_id`) REFERENCES `datasets` (`id`)), `question` (TEXT NOT NULL), `correct_answer` (TEXT NOT NULL), `choice1` (TEXT NOT NULL), `choice2` (TEXT NOT NULL), `choice3` (TEXT NOT NULL), `choice4` (TEXT NOT NULL), `choice5` (TEXT).
    *   Initialization: Automatically create the database and tables if they don't exist on application startup.
```
Tính năng này đã tự động thêm những chi tiết rất technical vào đoạn prompt phát thảo của tác giả:
- Python base image cho container
- Requirement file
- Persistence volume
- Port
- Tự thiết kế schema cho database
- ...

### Yêu cầu Architecture thiết kế hệ thống
Sau khi đã hài lòng với đoạn prompt cung cấp thông tin `công nghệ cần sử dụng` và `các tính năng cần có` của web app, tác giả dùng `AI Agent Architecture` để thiết kế chi tiết hệ thống. Architecture này cũng đảm nhiệm vai trò phân tách các giai đoạn làm việc để đảm bảo `AI Agent Developer` sẽ dễ dàng thực hiện.
