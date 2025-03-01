package TreeNodeProblems;
import java.util.Deque;
import java.util.LinkedList;

public class TreeNode {
    int val;
    TreeNode left;
    TreeNode right;

    TreeNode() {
    }

    TreeNode(int val) {
        this.val = val;
    }

    TreeNode(int val, TreeNode left, TreeNode right) {
        this.val = val;
        this.left = left;
        this.right = right;
    }

    static TreeNode of(Integer... vals) {
        if (vals.length == 0) {
            return new TreeNode();
        }

        TreeNode root = new TreeNode(vals[0]);
        Deque<TreeNode> leaves = new LinkedList<>();
        leaves.push(root);

        for (int i = 1; i < vals.length; i++) {
            Integer valLeft = vals[i];
            Integer valRight = null;
            if (i < vals.length - 1) {
                valRight = vals[++i];
            }
            var leaf = leaves.removeLast();
            if (valLeft != null) {
                var node = new TreeNode(valLeft);
                leaf.left = node;
                leaves.push(node);
            }
            if (valRight != null) {
                var node = new TreeNode(valRight);
                leaf.right = node;
                leaves.push(node);
            }
        }
        return root;
    }
}
