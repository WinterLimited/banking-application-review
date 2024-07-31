document.addEventListener("DOMContentLoaded", function () {
    document.querySelector(".tablinks").click();
    setupCustomSelect();
    filterReviews();  // Call filterReviews initially to load Google Play reviews by default
});

function setupCustomSelect() {
    var x, i, j, selElmnt, a, b, c;
    x = document.getElementsByClassName("custom-select");
    for (i = 0; i < x.length; i++) {
        selElmnt = x[i].getElementsByTagName("select")[0];
        a = document.createElement("DIV");
        a.setAttribute("class", "select-selected");
        a.innerHTML = selElmnt.options[selElmnt.selectedIndex].innerHTML;
        x[i].appendChild(a);
        b = document.createElement("DIV");
        b.setAttribute("class", "select-items select-hide");
        for (j = 0; j < selElmnt.length; j++) {
            c = document.createElement("DIV");
            c.innerHTML = selElmnt.options[j].innerHTML;
            c.addEventListener("click", function(e) {
                var y, i, k, s, h;
                s = this.parentNode.parentNode.getElementsByTagName("select")[0];
                h = this.parentNode.previousSibling;
                for (i = 0; i < s.length; i++) {
                    if (s.options[i].innerHTML == this.innerHTML) {
                        s.selectedIndex = i;
                        h.innerHTML = this.innerHTML;
                        y = this.parentNode.getElementsByClassName("same-as-selected");
                        for (k = 0; k < y.length; k++) {
                            y[k].removeAttribute("class");
                        }
                        this.setAttribute("class", "same-as-selected");
                        filterReviews();
                        break;
                    }
                }
                h.click();
            });
            b.appendChild(c);
        }
        x[i].appendChild(b);
        a.addEventListener("click", function(e) {
            e.stopPropagation();
            closeAllSelect(this);
            this.nextSibling.classList.toggle("select-hide");
            this.classList.toggle("select-arrow-active");
        });
    }
}

function closeAllSelect(elmnt) {
    var x, y, i, arrNo = [];
    x = document.getElementsByClassName("select-items");
    y = document.getElementsByClassName("select-selected");
    for (i = 0; i < y.length; i++) {
        if (elmnt == y[i]) {
            arrNo.push(i);
        } else {
            y[i].classList.remove("select-arrow-active");
        }
    }
    for (i = 0; i < x.length; i++) {
        if (arrNo.indexOf(i)) {
            x[i].classList.add("select-hide");
        }
    }
}

document.addEventListener("click", closeAllSelect);

function openBank(evt, bank) {
    var i, tabcontent, tablinks;

    // Hide all tabcontent
    tabcontent = document.getElementsByClassName("tabcontent");
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Remove active class from all tablinks
    tablinks = document.getElementsByClassName("tablinks");
    for (i = 0; i < tablinks.length; i++) {
        tablinks[i].className = tablinks[i].className.replace(" active", "");
    }

    // Show the current tab and add an "active" class to the button that opened the tab
    evt.currentTarget.className += " active";

    // Fetch and display reviews for the selected bank
    fetchReviews(bank.trim());
}

function filterReviews() {
    var bank = document.querySelector(".tablinks.active").textContent;
    fetchReviews(bank.trim());
}

function fetchReviews(bank) {
    var platform = document.getElementById("platform").value;
    fetch(`/get_reviews?bank=${encodeURIComponent(bank)}&platform=${encodeURIComponent(platform)}`)
        .then(response => response.json())
        .then(reviews => {
            // Sort reviews by date in descending order
            reviews.sort((a, b) => new Date(b.date) - new Date(a.date));
            displayReviews(bank, reviews);
        });
}

function displayReviews(bank, reviews) {
    var reviewsContainer = document.getElementById("reviews-container");
    var averageRating = reviews.length ? (reviews.reduce((acc, review) => acc + review.rating, 0) / reviews.length).toFixed(2) : 'N/A';

    reviewsContainer.innerHTML = `
        <div id="${bank}" class="tabcontent" style="display: block;">
            <h2>${bank} 
                <span class="avg-rating">평균 평점: ${displayStars(averageRating)} (${averageRating})</span>
            </h2>
            <table>
                <tr>
                    <th>작성자</th>
                    <th>평점</th>
                    <th>작성 내용</th>
                    <th>날짜</th>
                </tr>
                ${reviews.map(review => `
                <tr>
                    <td>${review.user_name}</td>
                    <td class="star-rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</td>
                    <td>${review.review}</td>
                    <td style="width: 200px">${formatDate(new Date(review.date))}</td>
                </tr>
                `).join('')}
            </table>
        </div>
    `;
}

function displayStars(rating) {
    const fullStars = Math.floor(rating);
    const halfStar = rating - fullStars >= 0.5 ? 1 : 0;
    const emptyStars = 5 - fullStars - halfStar;

    return '★'.repeat(fullStars) + '☆'.repeat(halfStar) + '☆'.repeat(emptyStars);
}

function formatDate(date) {
    return date.toLocaleDateString('ko-KR', {
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit'
    }).replace('.', '년').replace('.', '월').replace('.', '일');
}