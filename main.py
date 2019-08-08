import merge
import lda
# import select
# import vocabulary

if __name__ == '__main__':
    merge.get_data()
    merge.data_merge()
    lda.run()
