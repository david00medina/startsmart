from pycocotools.coco import COCO as cocoapi
import matplotlib as plt
import skimage.io as io


class COCO:
    def __init__(self, data_dir, ann_type, data_type, data_year, category_selection=None):
        self.__ann_file = '{}/{}_{}{}.json'.format(data_dir, ann_type, data_type, data_year)
        self.__COCO = cocoapi(self.__ann_file)
        self.__image_ids = None
        self.__category_info = None
        self.select_category(category_selection)
        self.__image_info = None
        self.__ann_selection = None
        self.__image = None

    @property
    def coco(self):
        return self.__COCO

    @property
    def image_ids(self):
        return self.__image_ids

    @property
    def total_images(self):
        return len(self.image_ids)

    @property
    def category_info(self):
        return self.__category_info

    @property
    def image_info(self):
        return self.__image_info

    @property
    def image(self):
        return self.__image

    @property
    def annotations(self):
        return self.__ann_selection

    def select_category(self, category_selection=None):
        if category_selection is None:
            print('Please select a category from the ones listed below:')
            cats = self.coco.loadCats(self.coco.getCatIds())
            print([cat['name'] for cat in cats])
        else:
            self.__category_info = self.coco.getCatIds(catNms=category_selection)
            self.__image_ids = self.coco.getImgIds(catIds=self.category_info)

    def select_image(self, image_no):
        if self.image_ids is None:
            return

        self.__image_info = self.coco.loadImgs(self.image_ids[image_no])[0]
        self.__image = io.imread(self.image_info['coco_url'])
        self.__select_annotations()

    def __select_annotations(self):
        if self.image_info is None or self.category_info is None:
            return

        annIds = self.coco.getAnnIds(imgIds=self.image_info['id'], catIds=self.category_info, iscrowd=None)
        self.__ann_selection = self.coco.loadAnns(annIds)

    def show_image(self):
        if self.image is None:
            return

        plt.axis('off')
        plt.imshow(self.image)
        plt.show()

    def show_annotations(self):
        if self.annotations is None:
            return

        self.coco.showAnns(self.annotations)
