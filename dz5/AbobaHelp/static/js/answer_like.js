async function handleAnswerLikeResponse(response, answer, like, dislike, rating) {
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


const answers = document.querySelectorAll("[data-type='answer']")
for (a of answers) {
    const answer = a
    const like = answer.querySelector("[data-type='answer-like']")
    const dislike = answer.querySelector("[data-type='answer-dislike']")
    const rating = answer.querySelector("[data-type='answer-rating']")
    if (!like || !dislike || !rating) {
        continue
    }

    like.addEventListener("click", async () => {
        console.log(answer)
        const response = await fetch(`/answer/${answer.dataset.id}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "content-type": "application/json",
            },
            body: JSON.stringify({
                like: 1
            })
        })
        handleAnswerLikeResponse(response, answer, like, dislike, rating)
    })
    dislike.addEventListener("click", async () => {
        const response = await fetch(`/answer/${answer.dataset.id}/like/`, {
            method: "POST",
            headers: {
                "X-CSRFToken": csrf,
                "content-type": "application/json",
            },
            body: JSON.stringify({
                like: -1
            })  
        })
        handleAnswerLikeResponse(response, answer, like, dislike, rating)
    })
}