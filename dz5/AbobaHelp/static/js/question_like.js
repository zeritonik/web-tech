async function handleQuestionLikeResponse(response, question, like, dislike, rating) {
    if (!response.ok) {
        alert("Error")
        return
    }
    const data = await response.json()
    if (data.status == "error") {
        alert(data.message)
        return
    }
    rating.innerHTML = data.rating
    like.style.display = "none"
    dislike.style.display = "none"
}


const questions = document.querySelectorAll("[data-type='question']")
for (q of questions) {
    const question = q
    const like = question.querySelector("[data-type='question-like']")
    const dislike = question.querySelector("[data-type='question-dislike']")
    const rating = question.querySelector("[data-type='question-rating']")
    if (!like || !dislike || !rating) {
        continue
    }

    like.addEventListener("click", async () => {
        console.log(question)
        const response = await fetch(`/question/${question.dataset.id}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "content-type": "application/json",
            },
            body: JSON.stringify({
                like: 1
            })
        })
        handleQuestionLikeResponse(response, question, like, dislike, rating)
    })
    dislike.addEventListener("click", async () => {
        const response = await fetch(`/question/${question.dataset.id}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "content-type": "application/json",
            },
            body: JSON.stringify({
                like: -1
            })  
        })
        handleQuestionLikeResponse(response, question, like, dislike, rating)
    })
}