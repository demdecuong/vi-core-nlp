def batch_computeF1(labels, preds, seq_lengths):
    same_num = 0
    label_num = 0
    pred_num = 0
    for i in range(len(labels)):
        label = labels[i]
        pred = preds[i]
        true_len = seq_lengths[i].item()
        pred = pred[:true_len, :true_len]
        label = label[:true_len, :true_len]
        predict_entity, label_entity = get_entities(pred, label)

        count = count_same_entities(label_entity, predict_entity)
        same_num += count
        label_num += len(label_entity)
        pred_num += len(predict_entity)
    precision = float(same_num/label_num)
    if pred_num > 0:
        recall = float(same_num/pred_num)
    else:
        recall = 0

    if precision+ recall>0:
        score = 2*precision*recall/(precision+recall)
    else:
        score = 0

    return score, precision, recall

def count_same_entities(label_items, pred_items):
    count = 0
    for item in label_items:
        if item in pred_items:
            count += 1
    return count

def get_entities(input_tensor, label):

    input_tensor, cate_pred = input_tensor.max(dim=-1)
    predict_entity = get_entity(cate_pred)
    label_entity = get_entity(label)
    return predict_entity, label_entity


def get_entity(input_tensor):
    entity = []
    for i in range(len(input_tensor)):
        for j in range(i,len(input_tensor)):
            if input_tensor[i][j] > 0:
                tmp = [i, j, input_tensor[i][j]]
                entity.append(tmp)
    return entity