class Cookie {
    constructor(cookieName) {
        this.cookieName = cookieName;
    }

    getValue() {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, this.cookieName.length + 1) === (this.cookieName + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(this.cookieName.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
}

export default Cookie;
