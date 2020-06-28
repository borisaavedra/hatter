function get_since(tagId){
    let nodelist = document.getElementsByTagName("SMALL").length
    let list = document.getElementsByTagName("SMALL")
    let now = Date.now()
    const days = 24 * 60 * 60 * 1000
    for (let i = 0; i < nodelist; i++){
      if (list[i].getAttribute("id") == tagId){
        let date_db = list[i].innerHTML
        let parsed_date = Date.parse(date_db)
        let since_ms = now - parsed_date
        let since = since_ms / days
          if (since <= 2){
            list[i].innerHTML = "1 day"
          }else{
            list[i].innerHTML = Math.trunc(since) + " days"
          }
      }
    }
  }