(function(global, document) {

    var NUM_ENTRIES = 3,
        URL = "http://rss.allabout.co.jp/aa/latest/",
        OUTPUT_ID = "feed",
        DEFAULT_IMAGE = 'static/img/no_image.png',
        BASE_ENTRY_HTML = '<div class="feed">\n'
            + '  <div class="pure-g feed__inner">\n'
            + '    <div class="pure-u-1 pure-u-md-1-4 section-part feed__image">\n'
            + '      <a href="{link}" target="_blank"><img src="{img}"></a>\n'
            + '    </div>\n'
            + '    <div class="pure-u-1 pure-u-md-3-4 section-part feed__contents">\n'
            + '      <h4><a href="{link}" target="_blank">{title}</a></h4>\n'
            + '      <div class="feed__summary">\n'
            + '          {summary}\n'
            + '      </div>\n'
            + '      <div class="feed__data">{categories}({date})</div>\n'
            + '    </div>\n'
            + '  </div>\n'
            + '</div>\n';

    var format = function(string, dict) {
        var string = string.replace();
        for (key in dict) {
            string = string.split('{' + key + '}').join(dict[key]);
        }
        return string;
    };

    function formatDate(date, baseFormat) {
        var year = date.getFullYear(),
            month = date.getMonth() + 1,
            day = date.getDate();
        if(arguments.length < 2) {
            baseFormat = '{year}.{month}.{day}';
        }
        month = (month < 10 ? "0" + month : month);
        day = (day < 10 ? "0" + day : day)
        
        return format(baseFormat, {
            'year': year,
            'month': month,
            'day': day
        });
    }

    function makeEntryHTML(entry) {
        var date = formatDate(new Date(entry.publishedDate)),
            img = entry.content.match(/src="(.*?)"/igm),
            categories = '';
        img = img === null ? DEFAULT_IMAGE : img[0].replace('src=', '').split('"').join('');

        if (entry.categories.length > 0) {
            categories += entry.categories;
            categories += '  |  '
        }

        return format(BASE_ENTRY_HTML, {
            'img': img,
            'title': entry.title,
            'date': date,
            'link': entry.link,
            'categories': categories,
            'summary': entry.content.replace(/<("[^"]*"|'[^']*'|[^'">])*>/g, '').substring(0, 100) + '...'
        })
    }

    function init() {
        var suffix = formatDate(new Date(), '{year}{month}{day}'),
            feed = new global.google.feeds.Feed(URL + '?' + suffix),
            html = "",
            i = 0;
        feed.setNumEntries(NUM_ENTRIES);
        feed.load(function(result) {
            if (result.error) {
                console.log(result.error.code + ":" + result.error.message);
                return;
            }
            for (i = 0; i < result.feed.entries.length; i++) {
                html += makeEntryHTML(result.feed.entries[i]);
            }
            document.getElementById(OUTPUT_ID).innerHTML = html;
        });
    }

    global.google.load("feeds", "1");
    global.google.setOnLoadCallback(init);
}(this, this.document));