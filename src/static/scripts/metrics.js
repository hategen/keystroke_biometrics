export function processMetrics(batch) {
    const metrics = [];

    for (let i = 0; i < batch.length; i++) {
        if (batch[i].type === 'keydown') {
            for (let j = i + 1; j <= batch.length; j++) {
                if (
                    batch[j] &&
                    batch[j].key === batch[i].key &&
                    batch[j].type === 'keyup'
                ) {
                    const metric = {
                        ...batch[i],
                        keypressDuration: batch[j].timestamp - batch[i].timestamp,
                        keyDownTimestamp: batch[i].timestamp,
                        keyUpTimestamp: batch[j].timestamp
                    }
                    metrics.push(metric);
                    break;
                }
            }
        }
    }
    return metrics;
}