supported_comics = {
    "xkcd": (
        "http://xkcd.com/1/",
        "//div[@id='comic']//img/@src",
        "//a[@rel='next']/@href",
    ),
    "Nedroid": (
        "http://nedroid.com/2005/09/2210-whee/",
        "//div[@id='comic']/img/@src",
        "//div[@class='nav-next']/a/@href",
    ),
    "JL8": (
        "http://limbero.org/jl8/1",
        "//img[@alt='Comic']/@src",
        "//a[text()='>']/@href",
    ),
    "SMBC": (
        "http://www.smbc-comics.com/comic/2002-09-05",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "Blindsprings": (
        "http://www.blindsprings.com/comic/blindsprings-cover-book-one",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "TheAbominableCharlesChristopher": (
        "http://abominable.cc/post/44164796353/episode-one",
        "//div[@class='photo']//img/@src",
        "//span[@class='next_post']//@href",
    ),
    "GuildedAge": (
        "http://guildedage.net/comic/chapter-1-cover/",
        "//div[@id='comic']//img/@src",
        "//a[@class='navi comic-nav-next navi-next']/@href",
    ),
    "TalesOfElysium": (
        "http://ssp-comics.com/comics/toe/?page=1&mode=10",
        "//div[@id='ImageComicContainer']//img[contains(@src, 'comic')]/@src",
        "//a[button/@id='next10Button']/@href",
    ),
    "AmazingSuperPowers": (
        "http://www.amazingsuperpowers.com/2007/09/heredity/",
        "//div[@class='comicpane']/img/@src",
        "//a[@class='navi navi-next']/@href",
    ),
    "Gunshow": (
        "http://gunshowcomic.com/1",
        "//img[@class='strip']/@src",
        "//span[@class='snavb'][4]/a/@href",
    ),
    "Lackadaisy": (
        "http://www.lackadaisycats.com/comic.php?comicid=1",
        "//div[@id='content']/img/@src",
        "//div[@class='next']/a/@href",
    ),
    "WildeLife": (
        "http://www.wildelifecomic.com/comic/1",
        "//img[@id='cc-comic']/@src",
        "//a[@class='cc-next']/@href",
    ),
    "ElGoonishShive": (
        "http://www.egscomics.com/comic/2002-01-21",
        "//div[@id='cc-comicbody']//img/@src",
        "//a[@class='cc-next']/@href",
    ),
    "StandStillStaySilent": (
        "http://www.sssscomic.com/comic.php?page=1",
        "//img[@class='comicnormal']/@src",
        "//a[img[contains(@src, 'next')]]/@href",
    ),
}
