
        // Example list of values
        const list = [
                        "UED2901924", "UED2901724", "UED2901324", "UED2901024", "UED2900924",
                        "UED2901224", "UED2901824", "UED2900624", "UED2900224", "UED2901442",
                        "UED2900824", "UED2902424", "UED2901524", "UED2503924", "UED2900324",
                        "UED2900124", "UED2902024", "UED2902724", "UED2901624", "UED2900524",
                        "UED2900424", "UED2901124", "UED2900724", "UED2902624", "UED2507224",
                        "UED2902724", "UED2902324", "UED2902824", "UED2902224", "UED2902524",
                        "UED2902124"
        ];

        
        var a = document.getElementById('hidden');
        a.style.display = 'none';
        
        // function for submit button
        function checkInput() {
            const indnum = document.getElementById('indnum').value.trim().toUpperCase();
            
            // Check if the input is in the list
            if (list.includes(indnum) && !logged_in.includes(indnum)) {
                logged_in.concat(indnum);
                alert(`Your input is correct!`);
                errorMessage.style.display = 'none';
            } else {
                if (logged_in.includes(indnum)){
                    alert(`Your input is invalid or not included or already logged in`);
                    event.preventDefault();
                    errorMessage.style.display = 'block';
                    a.style.display = "block";
            }
            } 
            if ((indnum) === "") {
                alert("The input is empty")
            }
        }
        
        // function for searching slides
        function searchBar() {
            var input, filter, ul, li, a, i;
            input = document.getElementById("searchbar");
            filter = input.value.toUpperCase();
            ul = document.getElementById("menu");
            li = ul.getElementsByTagName("li");
            
            for (i = 0; i < li.length; i++) {
                a = li[i].getElementsByTagName("a")[0];
                if (a.innerHTML.toUpperCase().indexOf(filter) > -1) {
                    li[i].style.display = "";
                } else {
                    li[i].style.display = "none";
                }
            }
        }
        // function for timing for flash message
        const flashMsg = document.getElementById("flash-msg");
        if (flashMsg) {
            setTimeout(() => {
                flashMsg.classList.add("hide");
            }, 5000);
        }

        // function for sidebar
        //const sidebar = document.getElementById("sidebar");
        //const menuToggle = document.getElementById("menuToggle");
        //const closeBtn = document.getElementById("closeButton");
        
        //menuToggle.addEventListener("click", () => {
        //    sidebar.style.width = "250px";
        //});

        //closeBtn.addEventListener("click", () => {
        //    sidebar.style.width = "0";
        //});