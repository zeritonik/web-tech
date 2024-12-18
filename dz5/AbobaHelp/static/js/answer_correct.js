for (a of answers) {
    const answer = a
    const correct = answer.querySelector("[data-type='answer-correct']")
    correct.addEventListener("change", async () => {
        const response = await fetch(`/answer/${answer.dataset.id}/correct/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "content-type": "application/json",
            },
            body: JSON.stringify({
                correct: correct.checked
            })
        })
        if (!response.ok) {
            alert("Error")
            return
        }
        const data = await response.json()
        if (data.status == "error") {
            alert(data.message)
            return
        }
        correct.checked = data.correct
    })
}