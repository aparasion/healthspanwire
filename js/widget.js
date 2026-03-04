const SocialTimelineWidget = (() => {

  async function init(config) {
    const res = await fetch("feed.json");
    const posts = await res.json();

    const container = document.getElementById(config.containerId);

    container.innerHTML = posts
      .map(post => `
        <div class="stw-post">
          <div class="stw-header">
            <img src="${post.avatar}" class="stw-avatar"/>
            <div>
              <div class="stw-name">${post.name}</div>
              <div class="stw-meta">
                ${post.platform} • ${new Date(post.date).toLocaleString()}
              </div>
            </div>
          </div>
          <div class="stw-content">${post.content}</div>
        </div>
      `)
      .join("");
  }

  return { init };

})();
