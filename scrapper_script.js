function formatDate(dateString){
    // Estamos recibiendo una fecha tipo "Sunday, September 17, 2023 at 11:29:01 PM AST"
    // Primero, parsear la fecha
    let dateParts = dateString.split(" at ");
    let dateWithOutZone = dateParts[0];
    
    let fechaParseada = new Date(dateWithOutZone);
    
    // Obtener los componentes de la fecha
    let dia = fechaParseada.getDate().toString().padStart(2, '0');
    let mes = (fechaParseada.getMonth() + 1).toString().padStart(2, '0');
    let año = fechaParseada.getFullYear();
    let horas = fechaParseada.getHours().toString().padStart(2, '0');
    let minutos = fechaParseada.getMinutes().toString().padStart(2, '0');
    let segundos = fechaParseada.getSeconds().toString().padStart(2, '0');
    
    // Formatear la fecha en el formato deseado
    return `${año}-${mes}-${dia} ${horas}:${minutos}:${segundos}`;
};

function getSubredditTitle(){
    let title = document.querySelector(`h1`)?.innerHTML
    
    if (!title) {
        const  titlePosibleNodes = document.querySelectorAll(`[class*='font-bold']`) 
        const titleElement = Array.from(titlePosibleNodes).find(node => node.innerHTML.startsWith(`r/`));
        title = titleElement.innerHTML.slice(2)
    }   

    return title
};

function getVideosPosts(){
    let videosPost =  document.querySelectorAll(`shreddit-post`)

    if (!videosPost) {
        videosPost = document.querySelectorAll(`[data-testid='post-container']`)
    }

    return videosPost
};

function  convertPostToData(postElement){
    const videoUrl = postElement.querySelector(`shreddit-player`)?.getAttribute(`src`)
    
    if (!videoUrl){
        return
    }

    const title = postElement.querySelector(`[slot='title']`)?.innerHTML?.trim()
    const postUrl = `https://www.reddit.com${postElement?.getAttribute('permalink')}`  
    const amountOfVotes = postElement.shadowRoot.querySelector(`faceplate-number`)?.getAttribute(`number`)

    const timeElement = postElement.querySelector(`time`)
    const publishDate = timeElement?.getAttribute(`title`)
    const timeAgo = timeElement?.innerHTML?.replace(/<.*?>|\./g, '')


    return {
        'title': title,
        'publish_date':formatDate(publishDate),
        'time_ago': timeAgo,
        'votes': amountOfVotes,
        'url': videoUrl,
        'post_url': postUrl
    }
}; 

function getAllVideosData(){
    const title = getSubredditTitle()
    const videosPost = getVideosPosts()

    const videos = Array.from(videosPost).map(convertPostToData).filter(item => item);

    return {
        'subreddit_title': title,
        'amount_of_posts': videosPost.length,
        'amount_of_videos_post': videos.length,
        'video_posts': videos
    }
};

return getAllVideosData();