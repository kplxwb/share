import argparse

from trainer import Trainer, OPTIMIZER_LIST
from utils import init_logger, build_vocab, download_vgg_features, set_seed
from data_loader import load_data


def main(args):
    init_logger()
    set_seed(args)
    download_vgg_features(args)
    build_vocab(args)

    train_dataset = load_data(args, mode="train")
    dev_dataset = load_data(args, mode="dev")
    test_dataset = load_data(args, mode="test")

    trainer = Trainer(args, train_dataset, dev_dataset, test_dataset)

    if args.do_train:
        trainer.train()

    if args.do_eval:
        trainer.load_model()
        trainer.evaluate("test")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument("--data_dir", default="/root/fgw/NER-Multimodal-pytorch/data", 
                        type=str, help="The input data dir")
    #保存模型的路径
    parser.add_argument("--model_dir", default="/root/fgw/NER-Multimodal-pytorch/model", 
                        type=str, help="Path for saving model")
    #预训练词向量的路径
    parser.add_argument("--wordvec_dir", default="/root/fgw/NER-Multimodal-pytorch/wordvec", 
                        type=str, help="Path for pretrained word vector")
    parser.add_argument("--vocab_dir", default="/root/fgw/NER-Multimodal-pytorch/vocab", type=str)

    parser.add_argument("--train_file", default="/root/fgw/NER-Multimodal-pytorch/data/train",
                         type=str, help="Train file")
    parser.add_argument("--dev_file", default="/root/fgw/NER-Multimodal-pytorch/data/dev",
                         type=str, help="Dev file")
    parser.add_argument("--test_file", default="/root/fgw/NER-Multimodal-pytorch/data/test", 
                        type=str, help="Test file")
    #预训练词向量文件
    parser.add_argument("--w2v_file", default="/root/fgw/NER-Multimodal-pytorch/wordvec/word_vector_200d.vec",
                         type=str, help="Pretrained word vector file")
    #预处理图像特征的文件名
    parser.add_argument("--img_feature_file", default="/root/fgw/NER-Multimodal-pytorch/img_vgg_features.pt", type=str, 
                        help="Filename for preprocessed image features")

    parser.add_argument("--max_seq_len", default=35, type=int, help="Max sentence length")
    parser.add_argument("--max_word_len", default=30, type=int, help="Max word length")

    parser.add_argument("--word_vocab_size", default=23204, type=int, help="Maximum size of word vocabulary")
    parser.add_argument("--char_vocab_size", default=102, type=int, help="Maximum size of character vocabulary")

    parser.add_argument("--word_emb_dim", default=200, type=int, help="Word embedding size")
    parser.add_argument("--char_emb_dim", default=30, type=int, help="Character embedding size")
    parser.add_argument("--final_char_dim", default=50, type=int, help="Dimension of character cnn output")
    parser.add_argument("--hidden_dim", default=200, type=int, help="Dimension of BiLSTM output, att layer (denoted as k) etc.")

    parser.add_argument("--kernel_lst", default="2,3,4", type=str, help="kernel size for character cnn")
    parser.add_argument("--num_filters", default=32, type=int, help=" Number of filters for character cnn")

    parser.add_argument('--seed', type=int, default=7, help="random seed for initialization")
    parser.add_argument("--train_batch_size", default=32, type=int, help="Batch size for training")
    parser.add_argument("--eval_batch_size", default=64, type=int, help="Batch size for evaluation")
    parser.add_argument("--optimizer", default="adam", type=str, help="Optimizer selected in the list: " + ", ".join(OPTIMIZER_LIST.keys()))
    parser.add_argument("--learning_rate", default=0.01, type=float, help="The initial learning rate")
    parser.add_argument("--num_train_epochs", default=8, type=float, help="Total number of training epochs to perform.")
    parser.add_argument("--slot_pad_label", default="[pad]", type=str, help="Pad token for slot label pad (to be ignore when calculate loss)")
    parser.add_argument("--ignore_index", default=0, type=int,
                        help='Specifies a target value that is ignored and does not contribute to the input gradient')

    parser.add_argument('--logging_steps', type=int, default=250, help="Log every X updates steps.")
    parser.add_argument('--save_steps', type=int, default=250, help="Save checkpoint every X updates steps.")

    parser.add_argument("--do_train", action="store_true", help="Whether to run training.")
    parser.add_argument("--do_eval", action="store_true", help="Whether to run eval on the test set.")
    parser.add_argument("--no_cuda", action="store_true", help="Avoid using CUDA when available")
    parser.add_argument("--no_w2v", action="store_true", help="Not loading pretrained word vector")

    args = parser.parse_args()

    # For VGG16 img features (DO NOT change this part)
    args.num_img_region = 49
    args.img_feat_dim = 512
    
    main(args)
