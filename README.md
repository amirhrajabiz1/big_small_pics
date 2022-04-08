# big_small_pics
a function for remake a big picture with small pictures.

for fun:>

make_image_memory_less(cache_address="D:\ml-tmp", primary_image_address=r'image.jpg', directroy_address_of_images=r'D:\ml-tmp\imgs', output=r'image_new.jpg', split_size=80, chance_to_repeat=0.009)

parameters:


cache_address : this is the directory we want to create a cache file for small images in it. warning: make sure there is no cache directory in cache_address because that will be deleted. default=r'.'

primary_image_address : the absolute or relative address of primary(big) image. default=r'./prime.jpg'

directroy_address_of_images : the address of directory of small images.default=r'images'

output: the address and name of result picture.default=r'./primeout.jpg'

split_size: the size of square small pics in pixels. defalut=100

chance_to_repeat: a number beween 0 and 1. 0 means there is no chance to repeat an small image in big image and 1 means there is no limit to repeat and the range means the chance of repeat. default=0.5



