input_images = {
    'IU': 'https://upload.wikimedia.org/wikipedia/commons/thumb/3/33/IU_at_%22Midnight_Runners%22_VIP_premiere%2C_7_August_2017_03.jpg/800px-IU_at_%22Midnight_Runners%22_VIP_premiere%2C_7_August_2017_03.jpg',
    'Stephen Curry': 'https://www.si.com/.image/ar_233:100%2Cc_fill%2Ccs_srgb%2Cg_faces:center%2Cq_auto:good%2Cw_1920/MTg4MDIzNjkxMDA5ODYxNDE4/stephen-curry-smiles-iso.webp',
    'Syed Saddiq': 'https://media2.malaymail.com/uploads/articles/2018/2018-08/20180802YM21.jpg',
    'Zendaya': 'https://static.wikia.nocookie.net/euphoria-hbo/images/8/8e/Zendaya.2.jpg/revision/latest?cb=20220127161803',
    'Donald Trump': 'https://upload.wikimedia.org/wikipedia/commons/5/56/Donald_Trump_official_portrait.jpg',
    'Sundar Pichai': 'https://pbs.twimg.com/profile_images/864282616597405701/M-FEJMZ0_400x400.jpg',
    'Emma Watson': 'https://m.media-amazon.com/images/M/MV5BMTQ3ODE2NTMxMV5BMl5BanBnXkFtZTgwOTIzOTQzMjE@._V1_.jpg',
    'Terence Tao': 'https://s3.amazonaws.com/cms.ipressroom.com/173/files/20147/53e288debd26f511d800600e_Terence_Tao/Terence_Tao_c4560e18-0bf8-4bab-8daa-7e74d3acf907-prv.jpg',
    'Lisa Surihani': 'https://images.mubicdn.net/images/cast_member/547675/cache-685317-1623361891/image-w856.jpg',
    'Yao Ming': 'https://news.cgtn.com/news/3355544d3449444e326b7a4d7a41544e7a59444f31457a6333566d54/img/e6967a2c66714597b9066901f652b6ee/e6967a2c66714597b9066901f652b6ee.jpg',
    'Aamir Khan': 'https://feeds.abplive.com/onecms/images/uploaded-images/2022/03/23/805edeaae1dd1bf1eb1d7e987595008c_original.jpg?impolicy=abp_cdn&imwidth=720',
    'Alice Kaushik': 'https://starsunfolded.com/wp-content/uploads/2017/09/Alice-Kaushik-_-Profile.jpg',
    'Aragaki Yui': 'https://myasianartist.com/pics/01/nihon-01-15.jpg',
    'Benedict Cumberbatch': 'https://cdn.britannica.com/05/187505-050-6BB9F835/Benedict-Cumberbatch-2014.jpg',
    'Cho Yi Hyun': 'https://lh3.googleusercontent.com/f1EWhzVT3dsDmgfVWPd95gK3j-4xxjl64DexnOB4Y_yA0rDlySu_vgib7k9Eq1TnKxdVhDp7nRHqWkKsnOAAr8JWcHyH9wB7hywjcSGCbF8B7w=w960-rj-l80-nu-e365',
    'Dagogo Altraide': 'https://pbs.twimg.com/profile_images/1354939470592700421/eOY88usY_400x400.jpg',
    'David Schwimmer': 'https://lookingglasstheatre.org/wp-content/uploads/2017/03/DAVID-SCHWIMMER.jpg',
    'Dua Lipa': 'https://resize.elle.fr/square_960_webp/var/plain_site/storage/images/beaute/cheveux/stars/dua-lipa-adopte-la-coupe-la-plus-elegante-du-moment-3977721/95844938-1-fre-FR/Dua-Lipa-adopte-la-coupe-la-plus-elegante-du-moment.jpg',
    'Dwayne Johnson': 'https://static.wikia.nocookie.net/jumanji/images/f/f1/Dwayne_Johnson_2%2C_2013.jpg/revision/latest?cb=20180209165525',
    'Elizabeth Olsen': 'https://s3.r29static.com/bin/entry/807/340x408,85/1830446/image.webp',
    'Elon Musk': 'https://thecampusjournal.com/wp-content/uploads/2022/04/hZ7zMKe9zRowML1P1hHKai4vJd9NPqyBrUWabUSa-900x900.jpeg',
    'Eliud Kipchoge': 'https://www.thesun.co.uk/wp-content/uploads/2019/10/NINTCHDBPICT000529746999jpg',
    'Viktor Axelsen': 'https://yonex-fareast.com/wp-content/uploads/2021/11/Axelsen_Tall_2_400x560-201909_1_.jpg',
    'Folorunso Alakija': 'https://www.blackpast.org/wp-content/uploads/Folorunsho_Alakija.jpg',
    'Francoise Meyers': 'https://www.tbsnews.net/sites/default/files/styles/infograph/public/images/2022/04/11/loreal_francoise_bettencourt_meyers.jpg',
    'Gal Gadot': 'https://media.gq.com/photos/5a0b201485eb8b728aa3ba99/3:4/w_999,h_1332,c_limit/gq-gal-gadot-accent.jpg',
    'Kim Tae-ri': 'https://images.news18.com/ibnlive/uploads/2022/03/kim-tae-ri.jpg',
    'Kim Jong-kook': 'https://zapzee.net/wp-content/uploads/2022/02/kimjongkook.jpg',
    'Josh Carrott': 'https://thumb.zigi.id/frontend/thumbnail/2021/09/06/zigi-6135cdca906f1-josh-carrott_910_512.jpg',
    'Keanu Reeves': 'https://m.media-amazon.com/images/M/MV5BNmNlNGU0ZDgtMDg3MS00ZGZmLTg4ZjMtYjMyZjVmNzlhNWIwXkEyXkFqcGdeQXVyMTE1MTYxNDAw._V1_UY1200_CR285,0,630,1200_AL_.jpg',
    'Keith Gill': 'https://media.marketrealist.com/brand-img/_hmiVuT7n/0x0/keith-gill-1613770659413.jpg',
    'Kim Kardashian': 'https://www.theartistree.fm/wp-content/uploads/2022/03/Kim-Kardashian-1.jpg',
    'Lalisa Manobal': 'https://s1.ibtimes.com/sites/www.ibtimes.com/files/styles/full/public/2021/05/27/blackpink-member-lisa.jpg',
    'Lee Jong-suk': 'https://upload.wikimedia.org/wikipedia/commons/2/2e/Lee_Jong-suk_March_2018.png',
    'Lee Kwang-soo': 'https://pbs.twimg.com/profile_images/1243927716333645824/EG6Cl-Qg_400x400.jpg',
    'Linus Torvalds': 'https://cdn.britannica.com/99/124299-050-4B4D509F/Linus-Torvalds-2012.jpg',
    'Lionel Messi': 'https://cdn.images.express.co.uk/img/dynamic/67/590x/Lionel-Messi-contract-Barcelona-transfer-news-gossip-1463739.jpg',
    'Malala Yousafzai': 'https://womenscenter.unc.edu/wp-content/uploads/sites/349/2017/03/Malala-Yousafzai_Antonio-Olmos.jpg',
    'Martin Luther King Jr.': 'https://www.history.com/.image/ar_16:9%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTc4MDk1MTkzMzUyODQwODEz/martin-luther-king-jr-gettyimages-517481130.jpg',
    'Albert Einstein': 'https://insidetheperimeter.ca/wp-content/uploads/2015/11/Albert_einstein_by_zuzahin-d5pcbug-WikiCommons.jpg',
    'Morgan Freeman': 'https://cdn.britannica.com/40/144440-050-DA828627/Morgan-Freeman.jpg',
    'Neil Tyson': 'https://cdn.britannica.com/06/202006-050-64C85CC7/Neil-deGrasse-Tyson-2018.jpg',
    'Park Solomon': 'https://i0.wp.com/www.globalgranary.life/wp-content/uploads/2022/02/Park-solomon-e1643757573666.jpeg',
    'Queen Elizabeth II': 'https://upload.wikimedia.org/wikipedia/commons/thumb/b/b6/Queen_Elizabeth_II_in_March_2015.jpg/1200px-Queen_Elizabeth_II_in_March_2015.jpg',
    'Robert Downey Jr.': 'https://www.namesbiography.com/wp-content/uploads/2020/07/Robert-Downey.jpg',
    'Rowan Atkinson': 'https://caknowledge.com/wp-content/uploads/2021/09/Rowan-Atkinson-Net-Worth.jpeg',
    'Sabrina Azhar': 'https://yt3.ggpht.com/ytc/AKedOLQMvYm8ejBMsb2l8c6LvMgbFvUqgf_jGljB7jmxmA=s900-c-k-c0x00ffffff-no-rj',
    'Anthony Wong': 'https://m.thepeninsulaqatar.com/get/maximage/20190602_1559502359-226025.jpg',
    'Scha Alyahya': 'https://www.cinema.com.my/images/news/2011/7int_schaboy00.jpg',
    "Shaquille O'Neal": 'https://www.wpri.com/wp-content/uploads/sites/23/2021/01/20196639825152.jpg',
    'Simone Biles': 'https://simonebiles.com/wp-content/uploads/2021/08/slide-01-background-1920x1080-2.jpg',
    'Stephen Hawking': 'https://www.biography.com/.image/ar_4:3%2Cc_fill%2Ccs_srgb%2Cfl_progressive%2Cq_auto:good%2Cw_1200/MTY2MzU1NDM3Mzg4NTcyMzM0/stephen-hawking-on-october-10-1979-in-princeton-new-jersey-photo-by-santi-visalligetty-images.jpg',
    'Taylor Swift': 'https://www.scoutmag.ph/wp-content/uploads/2022/03/Dr.-Taylor-Swift-is-in-NYU-grants-her-an-honorary-doctorate.jpg',
    'Tiger Woods': 'https://static.onecms.io/wp-content/uploads/sites/20/2021/01/19/tiger-woods-2000.jpg',
    'Usain Bolt': 'https://static.onecms.io/wp-content/uploads/sites/20/2021/07/21/Usain-Bolt-1-2000.jpg',
    'Vivy Yusof': 'https://murai.my/wp-content/uploads/2018/04/Screen-Shot-2018-04-02-at-11.45.24-AM.png',
    'Wang Yibo': 'https://6.vikiplatform.com/image/9507e4abf00542b2b73c5f66b1ddd93d.jpg',
    'Warren Buffett': 'https://cdn.gobankingrates.com/wp-content/uploads/2022/01/berkshire-hathaway-chairman-ceo-warren-buffett_shutterstock_editorial_10227728a.jpg',
    'Will Smith': 'https://static.onecms.io/wp-content/uploads/sites/20/2021/11/02/will-smith-2019-2000.jpg',
    'Yeji': 'https://cdn.realsport101.com/images/ncavvykf/epicstream/af2f32044eb1cd4f2e6d4c7a9c8335035fc0d2f7-512x270.jpg',
    'Yvette Simpson': 'https://media.bizj.us/view/img/10440792/simpsonyvette2017*750xx600-800-0-0.jpg',
    'Jack Ma': 'https://image.cnbcfm.com/api/v1/image/104225995-_95A5004.jpg',
    'Namewee': 'https://i.malaysiakini.com/1198/4d25fd456256d2bb2902e5b742a9550b.jpeg',
    'Joanne Missingham': 'https://attach.setn.com/newsimages/2020/04/10/2497317-PH.jpg',
    'Isabel Peron': 'https://static.wikia.nocookie.net/totalwar-ar/images/3/33/Isabel_Peron.jpg/revision/latest?cb=20180703074154',
}

import base64
import concurrent.futures
import io
import json
import urllib

import cv2
import numpy as np
import PIL
from sklearn.decomposition import PCA

from frame_analyzer import FrameAnalyzer
import face

def download_image(url):
    try:
        with urllib.request.urlopen(url) as req:
            return np.asarray(bytearray(req.read()), dtype=np.uint8)
    except:
        print('Failed to download image', url)
        return None

with concurrent.futures.ThreadPoolExecutor() as executor:
    downloaded_images = {
        name: executor.submit(download_image, url)
        for name, url in input_images.items()
    }
downloaded_images = {name: fut.result() for name, fut in downloaded_images.items() if fut.result() is not None}

fa = FrameAnalyzer(init_classifiers=False, init_mp_hands=False)
fa.face_classifier = face.FaceClassifier()
def encode_image(np_img):
    global fa
    img = cv2.imdecode(np_img, -1)
    fa.set_frame(img, 'BGR')
    fa.frame = FrameAnalyzer.standardize_frame_size(fa.frame)
    buffer = io.BytesIO()
    PIL.Image.fromarray(fa.frame).save(buffer, format='PNG')
    b64_img = 'data:image/png;base64,' + base64.b64encode(buffer.getvalue()).decode('utf-8')
    enc_face = fa._get_face_encoding()
    return b64_img, enc_face

output_json = {}
for name, np_img in downloaded_images.items():
    print(name)
    b64_img, enc_face = encode_image(np_img)
    output_json[name] = {
        'link': input_images[name],
        'a128': enc_face.tolist(),
        'b64': b64_img,
    }

X = np.array([info['a128'] for info in output_json.values()])
pca = PCA(n_components=3).fit(X)
X_pca = pca.transform(X)
for i, name in enumerate(output_json):
    output_json[name]['pca'] = X_pca[i].tolist()

with open('encoded_faces.json', 'w') as file:
    json.dump(output_json, file)
