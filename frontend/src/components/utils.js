import config from "@/config"

export const getImageUrl = url =>{
    if (url.match(config.imageUrl)) {
      return url
    } else {
      return config.imageUrl + url
    }
  }
